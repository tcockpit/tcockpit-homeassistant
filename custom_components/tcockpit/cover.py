"""Covers matching Tessie: trunk, frunk, charge port, windows. Buttons remain for one-shots."""
from __future__ import annotations

from homeassistant.components.cover import CoverDeviceClass, CoverEntity, CoverEntityFeature
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .entity import TCockpitEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        vin = v["vin"]
        if c.can("trunk"):
            ents.append(TrunkCover(c, vin))
        if c.can("frunk"):
            ents.append(FrunkCover(c, vin))
        if c.can("open_charge_port") or c.can("close_charge_port"):
            ents.append(ChargePortCover(c, vin))
        if c.can("vent_windows") or c.can("close_windows"):
            ents.append(WindowsCover(c, vin))
    async_add_entities(ents)


class TrunkCover(TCockpitEntity, CoverEntity):
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_supported_features = CoverEntityFeature.OPEN  # Tesla trunk is toggle/open

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "trunk_cover")

    @property
    def is_closed(self):
        open_ = self.state_data.get("trunkOpen")
        return None if open_ is None else (not open_)

    async def async_open_cover(self, **kwargs) -> None:
        if not self.coordinator.can("trunk"):
            raise HomeAssistantError("Trunk needs Entriegeln permission")
        await self.coordinator.api.command(self.vin, "trunk")
        await self.coordinator.async_request_refresh()


class FrunkCover(TCockpitEntity, CoverEntity):
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_supported_features = CoverEntityFeature.OPEN

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "frunk_cover")

    @property
    def is_closed(self):
        open_ = self.state_data.get("frunkOpen")
        return None if open_ is None else (not open_)

    async def async_open_cover(self, **kwargs) -> None:
        if not self.coordinator.can("frunk"):
            raise HomeAssistantError("Frunk needs Entriegeln permission")
        await self.coordinator.api.command(self.vin, "frunk")
        await self.coordinator.async_request_refresh()


class ChargePortCover(TCockpitEntity, CoverEntity):
    _attr_device_class = CoverDeviceClass.DOOR
    _attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "charge_port_cover")

    @property
    def is_closed(self):
        open_ = self.state_data.get("chargePortOpen")
        return None if open_ is None else (not open_)

    async def async_open_cover(self, **kwargs) -> None:
        if not self.coordinator.can("open_charge_port"):
            raise HomeAssistantError("Opening charge port needs Entriegeln")
        await self.coordinator.api.command(self.vin, "open_charge_port")
        await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs) -> None:
        if not self.coordinator.can("close_charge_port"):
            raise HomeAssistantError("Closing charge port needs Steuern")
        await self.coordinator.api.command(self.vin, "close_charge_port")
        await self.coordinator.async_request_refresh()


class WindowsCover(TCockpitEntity, CoverEntity):
    _attr_device_class = CoverDeviceClass.WINDOW
    _attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "windows_cover")

    @property
    def is_closed(self):
        open_ = self.state_data.get("windowsOpen")
        return None if open_ is None else (not open_)

    async def async_open_cover(self, **kwargs) -> None:
        if not self.coordinator.can("vent_windows"):
            raise HomeAssistantError("Venting windows needs Entriegeln")
        await self.coordinator.api.command(self.vin, "vent_windows")
        await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs) -> None:
        if not self.coordinator.can("close_windows"):
            raise HomeAssistantError("Closing windows needs Steuern")
        await self.coordinator.api.command(self.vin, "close_windows")
        await self.coordinator.async_request_refresh()
