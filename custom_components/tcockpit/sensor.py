"""Sensors: battery, range, charging, climate temperatures, odometer."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfEnergy, UnitOfLength, UnitOfPower, UnitOfPressure, UnitOfTemperature, UnitOfTime

from .const import DOMAIN
from .entity import TCockpitEntity


@dataclass(frozen=True, kw_only=True)
class Desc(SensorEntityDescription):
    field: str = ""


SENSORS = [
    Desc(key="battery_level", field="batteryLevel", device_class=SensorDeviceClass.BATTERY, native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="range", field="rangeKm", device_class=SensorDeviceClass.DISTANCE, native_unit_of_measurement=UnitOfLength.KILOMETERS, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="charging_state", field="chargingState"),
    Desc(key="charger_power", field="chargerPowerKW", device_class=SensorDeviceClass.POWER, native_unit_of_measurement=UnitOfPower.KILO_WATT, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="charge_limit", field="chargeLimitPercent", native_unit_of_measurement=PERCENTAGE),
    Desc(key="charge_energy_added", field="chargeEnergyAddedKWh", device_class=SensorDeviceClass.ENERGY, native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR, state_class=SensorStateClass.TOTAL),
    Desc(key="time_to_full", field="minutesToFullCharge", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement=UnitOfTime.MINUTES),
    Desc(key="inside_temp", field="insideTempC", device_class=SensorDeviceClass.TEMPERATURE, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="outside_temp", field="outsideTempC", device_class=SensorDeviceClass.TEMPERATURE, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="odometer", field="odometerKm", device_class=SensorDeviceClass.DISTANCE, native_unit_of_measurement=UnitOfLength.KILOMETERS, state_class=SensorStateClass.TOTAL_INCREASING),
    Desc(key="presence", field="presence"),
    Desc(key="address", field="address"),
    Desc(key="software", field="softwareVersion"),
]
TIRES = [("tire_fl", "frontLeft"), ("tire_fr", "frontRight"), ("tire_rl", "rearLeft"), ("tire_rr", "rearRight")]


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        ents += [TCockpitSensor(c, v["vin"], d) for d in SENSORS]
        ents += [TireSensor(c, v["vin"], k, f) for k, f in TIRES]
    async_add_entities(ents)


class TCockpitSensor(TCockpitEntity, SensorEntity):
    def __init__(self, coordinator, vin, desc: Desc) -> None:
        super().__init__(coordinator, vin, desc.key)
        self.entity_description = desc

    @property
    def native_value(self):
        return self.state_data.get(self.entity_description.field)


class TireSensor(TCockpitEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_native_unit_of_measurement = UnitOfPressure.BAR

    def __init__(self, coordinator, vin, key, field) -> None:
        super().__init__(coordinator, vin, key)
        self._field = field

    @property
    def native_value(self):
        return (self.state_data.get("tirePressureBar") or {}).get(self._field)
