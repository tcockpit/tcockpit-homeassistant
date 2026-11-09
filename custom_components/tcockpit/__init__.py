"""TCockpit integration for Home Assistant."""
from __future__ import annotations

from datetime import timedelta
import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import TCockpitApi, TCockpitAuthError, TCockpitError
from .const import CONF_API_KEY, CONF_URL, DEFAULT_URL, DOMAIN, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.SWITCH,
    Platform.LOCK,
    Platform.CLIMATE,
    Platform.NUMBER,
    Platform.BUTTON,
    Platform.SELECT,
    Platform.COVER,
    Platform.MEDIA_PLAYER,
    Platform.UPDATE,
]

SERVICE_SEND_COMMAND = "send_command"
SERVICE_VALET = "valet_mode"
SERVICE_SPEED_LIMIT = "speed_limit"
SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("vin"): cv.string,
        vol.Required("command"): cv.string,
        vol.Optional("parameters", default={}): dict,
    }
)
VALET_SCHEMA = vol.Schema(
    {
        vol.Required("vin"): cv.string,
        vol.Required("enabled"): cv.boolean,
        vol.Required("pin"): cv.string,
    }
)
SPEED_LIMIT_SCHEMA = vol.Schema(
    {
        vol.Required("vin"): cv.string,
        vol.Required("action"): vol.In(["activate", "deactivate", "clear_pin"]),
        vol.Required("pin"): cv.string,
    }
)


class TCockpitCoordinator(DataUpdateCoordinator[dict]):
    """Polls vehicles + optional energy sites. Reading never wakes a car."""

    def __init__(self, hass: HomeAssistant, api: TCockpitApi) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS))
        self.api = api
        self.vehicles: list[dict] = []
        self.info: dict = {}
        self.energy: dict = {}

    async def _async_update_data(self) -> dict:
        try:
            self.vehicles = await self.api.vehicles()
            vehicles = {v["vin"]: await self.api.state(v["vin"]) for v in self.vehicles}
            try:
                self.energy = await self.api.energy()
            except TCockpitError as err:
                _LOGGER.debug("energy fetch: %s", err)
                self.energy = {"hasScope": False, "sites": [], "error": str(err)}
            return {"vehicles": vehicles, "energy": self.energy}
        except TCockpitAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except TCockpitError as err:
            raise UpdateFailed(str(err)) from err

    def can(self, command: str) -> bool:
        return command in (self.info.get("commands") or [])

    def vehicle_state(self, vin: str) -> dict:
        data = self.data or {}
        return (data.get("vehicles") or {}).get(vin) or {}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = TCockpitApi(async_get_clientsession(hass), entry.data.get(CONF_URL, DEFAULT_URL), entry.data[CONF_API_KEY])
    coordinator = TCockpitCoordinator(hass, api)
    try:
        coordinator.info = await api.info()
    except TCockpitAuthError as err:
        raise ConfigEntryAuthFailed(str(err)) from err
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def _send_command(call: ServiceCall) -> None:
        vin = str(call.data["vin"]).upper()
        command = str(call.data["command"])
        params = call.data.get("parameters") or {}
        if not coordinator.can(command):
            raise HomeAssistantError(f"Command '{command}' not allowed for this API key")
        if vin not in {v["vin"] for v in coordinator.vehicles}:
            raise HomeAssistantError("Vehicle not found")
        try:
            await coordinator.api.command(vin, command, **params)
        except TCockpitError as err:
            raise HomeAssistantError(str(err)) from err
        await coordinator.async_request_refresh()

    async def _valet(call: ServiceCall) -> None:
        vin = str(call.data["vin"]).upper()
        pin = str(call.data["pin"])
        enabled = bool(call.data["enabled"])
        cmd = "valet_on" if enabled else "valet_off"
        if not coordinator.can(cmd):
            raise HomeAssistantError(f"Command '{cmd}' not allowed for this API key")
        if vin not in {v["vin"] for v in coordinator.vehicles}:
            raise HomeAssistantError("Vehicle not found")
        try:
            await coordinator.api.command(vin, cmd, pin=pin)
        except TCockpitError as err:
            raise HomeAssistantError(str(err)) from err
        await coordinator.async_request_refresh()

    async def _speed_limit(call: ServiceCall) -> None:
        vin = str(call.data["vin"]).upper()
        pin = str(call.data["pin"])
        action = str(call.data["action"])
        cmd = {
            "activate": "speed_limit_activate",
            "deactivate": "speed_limit_deactivate",
            "clear_pin": "speed_limit_clear_pin",
        }[action]
        if not coordinator.can(cmd):
            raise HomeAssistantError(f"Command '{cmd}' not allowed for this API key")
        if vin not in {v["vin"] for v in coordinator.vehicles}:
            raise HomeAssistantError("Vehicle not found")
        try:
            await coordinator.api.command(vin, cmd, pin=pin)
        except TCockpitError as err:
            raise HomeAssistantError(str(err)) from err
        await coordinator.async_request_refresh()

    if not hass.services.has_service(DOMAIN, SERVICE_SEND_COMMAND):
        hass.services.async_register(DOMAIN, SERVICE_SEND_COMMAND, _send_command, schema=SERVICE_SCHEMA)
        hass.services.async_register(DOMAIN, SERVICE_VALET, _valet, schema=VALET_SCHEMA)
        hass.services.async_register(DOMAIN, SERVICE_SPEED_LIMIT, _speed_limit, schema=SPEED_LIMIT_SCHEMA)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_SEND_COMMAND)
            if hass.services.has_service(DOMAIN, SERVICE_VALET):
                hass.services.async_remove(DOMAIN, SERVICE_VALET)
            if hass.services.has_service(DOMAIN, SERVICE_SPEED_LIMIT):
                hass.services.async_remove(DOMAIN, SERVICE_SPEED_LIMIT)
    return ok
