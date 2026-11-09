"""Numeric controls: charge limit and charging amps."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import PERCENTAGE, UnitOfElectricCurrent

from .const import DOMAIN
from .entity import TCockpitEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        if c.can("set_charge_limit"):
            ents.append(ChargeLimit(c, v["vin"]))
        if c.can("set_charge_current"):
            ents.append(ChargeAmps(c, v["vin"]))
    async_add_entities(ents)


class ChargeLimit(TCockpitEntity, NumberEntity):
    _attr_native_min_value = 50
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "charge_limit_set")

    @property
    def native_value(self):
        return self.state_data.get("chargeLimitPercent")

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.api.command(self.vin, "set_charge_limit", percent=int(value))
        await self.coordinator.async_request_refresh()


class ChargeAmps(TCockpitEntity, NumberEntity):
    _attr_native_min_value = 5
    _attr_native_max_value = 48
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "charge_amps")

    @property
    def native_max_value(self):
        mx = self.state_data.get("maxChargeCurrentAmps")
        return float(mx) if mx else 48.0

    @property
    def native_value(self):
        return self.state_data.get("chargeCurrentAmps")

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.api.command(self.vin, "set_charge_current", amps=int(value))
        await self.coordinator.async_request_refresh()
