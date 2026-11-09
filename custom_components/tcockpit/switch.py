"""Toggleable controls. Only created when the API key allows the matching command."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .entity import TCockpitEntity

# (unique_key, state_field, on_cmd, off_cmd)
ITEMS = [
    ("charging_switch", "charging", "charge_start", "charge_stop"),
    ("sentry", "sentryMode", "sentry_on", "sentry_off"),
    ("defrost", "defrostOn", "defrost_on", "defrost_off"),
    ("steering_wheel_heater", "steeringWheelHeat", "steering_wheel_heater_on", "steering_wheel_heater_off"),
    ("bioweapon", "bioweaponMode", "bioweapon_on", "bioweapon_off"),
    ("keep_accessory_power", "keepAccessoryPower", "keep_accessory_power_on", "keep_accessory_power_off"),
    ("cabin_overheat_protection", "cabinOverheatProtection", "cabin_overheat_protection_on", "cabin_overheat_protection_off"),
    ("low_power_mode", "lowPowerMode", "low_power_mode_on", "low_power_mode_off"),
    ("auto_steering_wheel_heat", "autoSteeringWheelHeat", "auto_steering_wheel_heat_on", "auto_steering_wheel_heat_off"),
]


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        for key, field, on_cmd, off_cmd in ITEMS:
            if c.can(on_cmd):
                ents.append(Control(c, v["vin"], key, field, on_cmd, off_cmd))
        if c.can("auto_seat_climate"):
            ents.append(AutoSeat(c, v["vin"], "auto_seat_climate_left", "autoSeatClimateLeft", 1))
            ents.append(AutoSeat(c, v["vin"], "auto_seat_climate_right", "autoSeatClimateRight", 2))
    async_add_entities(ents)


class Control(TCockpitEntity, SwitchEntity):
    def __init__(self, coordinator, vin, key, field, on_cmd, off_cmd) -> None:
        super().__init__(coordinator, vin, key)
        self._field, self._on, self._off = field, on_cmd, off_cmd

    @property
    def is_on(self):
        value = self.state_data.get(self._field)
        return None if value is None else bool(value)

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.api.command(self.vin, self._on)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.api.command(self.vin, self._off)
        await self.coordinator.async_request_refresh()


class AutoSeat(TCockpitEntity, SwitchEntity):
    def __init__(self, coordinator, vin, key, field, seat) -> None:
        super().__init__(coordinator, vin, key)
        self._field, self._seat = field, seat

    @property
    def is_on(self):
        value = self.state_data.get(self._field)
        return None if value is None else bool(value)

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.api.command(self.vin, "auto_seat_climate", seat=self._seat, on=True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.api.command(self.vin, "auto_seat_climate", seat=self._seat, on=False)
        await self.coordinator.async_request_refresh()
