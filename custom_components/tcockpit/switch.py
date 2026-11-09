"""Controls: climate and charging. Only created when the API key allows control.

A switch sends ONE command to the TCockpit server, which queues it exactly like a
command from the app (it may wake the car, retries, and pushes the result to your
iPhone). Nothing is sent automatically by this integration.
"""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .entity import TCockpitEntity

ITEMS = [("climate", "climateOn", "climate_on", "climate_off"), ("charging_switch", "charging", "charge_start", "charge_stop")]


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    if not c.can("climate_on"):
        return
    async_add_entities(Control(c, v["vin"], *item) for v in c.vehicles for item in ITEMS)


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
