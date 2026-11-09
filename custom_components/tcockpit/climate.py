"""Climate entity: on/off + target temperature (15–28 °C)."""
from __future__ import annotations

from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature, HVACMode
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature

from .const import DOMAIN
from .entity import TCockpitEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    if not c.can("climate_on"):
        return
    async_add_entities(VehicleClimate(c, v["vin"]) for v in c.vehicles)


class VehicleClimate(TCockpitEntity, ClimateEntity):
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT_COOL]
    _attr_min_temp = 15
    _attr_max_temp = 28
    _attr_target_temperature_step = 0.5
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "climate")

    @property
    def hvac_mode(self):
        on = self.state_data.get("climateOn")
        if on is None:
            return None
        return HVACMode.HEAT_COOL if on else HVACMode.OFF

    @property
    def current_temperature(self):
        return self.state_data.get("insideTempC")

    @property
    def target_temperature(self):
        return self.state_data.get("targetTempC")

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if hvac_mode == HVACMode.OFF:
            await self.coordinator.api.command(self.vin, "climate_off")
        else:
            await self.coordinator.api.command(self.vin, "climate_on")
        await self.coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs) -> None:
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is None:
            return
        await self.coordinator.api.command(self.vin, "set_temperature", celsius=float(temp))
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self) -> None:
        await self.async_set_hvac_mode(HVACMode.HEAT_COOL)

    async def async_turn_off(self) -> None:
        await self.async_set_hvac_mode(HVACMode.OFF)
