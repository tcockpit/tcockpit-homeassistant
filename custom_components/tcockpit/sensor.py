"""Sensors: vehicle telemetry + energy site / wall connector (read-only)."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import (
    PERCENTAGE, UnitOfElectricCurrent, UnitOfElectricPotential, UnitOfEnergy,
    UnitOfLength, UnitOfPower, UnitOfPressure, UnitOfSpeed, UnitOfTemperature, UnitOfTime,
)

from .const import DOMAIN
from .entity import TCockpitEntity, TCockpitEnergyEntity, TCockpitWallConnectorEntity


@dataclass(frozen=True, kw_only=True)
class Desc(SensorEntityDescription):
    field: str = ""


SENSORS = [
    Desc(key="battery_level", field="batteryLevel", device_class=SensorDeviceClass.BATTERY, native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="range", field="rangeKm", device_class=SensorDeviceClass.DISTANCE, native_unit_of_measurement=UnitOfLength.KILOMETERS, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="rated_range", field="ratedRangeKm", device_class=SensorDeviceClass.DISTANCE, native_unit_of_measurement=UnitOfLength.KILOMETERS, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="charging_state", field="chargingState"),
    Desc(key="charger_power", field="chargerPowerKW", device_class=SensorDeviceClass.POWER, native_unit_of_measurement=UnitOfPower.KILO_WATT, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="charger_voltage", field="chargerVoltageV", device_class=SensorDeviceClass.VOLTAGE, native_unit_of_measurement=UnitOfElectricPotential.VOLT, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="charger_amps", field="chargerActualAmps", device_class=SensorDeviceClass.CURRENT, native_unit_of_measurement=UnitOfElectricCurrent.AMPERE, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="charger_phases", field="chargerPhases", state_class=SensorStateClass.MEASUREMENT),
    Desc(key="charge_limit", field="chargeLimitPercent", native_unit_of_measurement=PERCENTAGE),
    Desc(key="charge_energy_added", field="chargeEnergyAddedKWh", device_class=SensorDeviceClass.ENERGY, native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR, state_class=SensorStateClass.TOTAL),
    Desc(key="time_to_full", field="minutesToFullCharge", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement=UnitOfTime.MINUTES),
    Desc(key="inside_temp", field="insideTempC", device_class=SensorDeviceClass.TEMPERATURE, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="outside_temp", field="outsideTempC", device_class=SensorDeviceClass.TEMPERATURE, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="driver_temp", field="driverTempC", device_class=SensorDeviceClass.TEMPERATURE, native_unit_of_measurement=UnitOfTemperature.CELSIUS),
    Desc(key="passenger_temp", field="passengerTempC", device_class=SensorDeviceClass.TEMPERATURE, native_unit_of_measurement=UnitOfTemperature.CELSIUS),
    Desc(key="odometer", field="odometerKm", device_class=SensorDeviceClass.DISTANCE, native_unit_of_measurement=UnitOfLength.KILOMETERS, state_class=SensorStateClass.TOTAL_INCREASING),
    Desc(key="speed", field="speedKmh", device_class=SensorDeviceClass.SPEED, native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="shift_state", field="shiftState"),
    Desc(key="presence", field="presence"),
    Desc(key="address", field="address"),
    Desc(key="software", field="softwareVersion"),
    Desc(key="destination", field="destination"),
    Desc(key="distance_to_arrival", field="remainingKm", device_class=SensorDeviceClass.DISTANCE, native_unit_of_measurement=UnitOfLength.KILOMETERS),
    Desc(key="time_to_arrival", field="minutesToArrival", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement=UnitOfTime.MINUTES),
    Desc(key="lifetime_energy_used", field="lifetimeEnergyUsedKWh", device_class=SensorDeviceClass.ENERGY, native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR, state_class=SensorStateClass.TOTAL_INCREASING),
    Desc(key="energy_remaining", field="energyRemainingKWh", device_class=SensorDeviceClass.ENERGY, native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="battery_health", field="batteryHealthPercent", native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="nominal_full_pack", field="nominalFullPackKWh", device_class=SensorDeviceClass.ENERGY, native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR),
    Desc(key="charge_cable", field="chargeCableType"),
    Desc(key="charge_port_latch", field="chargePortLatch"),
    # v0.4.0
    Desc(key="pack_voltage", field="packVoltageV", device_class=SensorDeviceClass.VOLTAGE, native_unit_of_measurement=UnitOfElectricPotential.VOLT, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="pack_current", field="packCurrentA", device_class=SensorDeviceClass.CURRENT, native_unit_of_measurement=UnitOfElectricCurrent.AMPERE, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="module_temp_max", field="moduleTempMaxC", device_class=SensorDeviceClass.TEMPERATURE, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="module_temp_min", field="moduleTempMinC", device_class=SensorDeviceClass.TEMPERATURE, native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="idle_loss_30d", field="idleLossKWh30d", device_class=SensorDeviceClass.ENERGY, native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="phantom_drain", field="phantomDrainPercent", native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="phantom_drain_per_day", field="phantomDrainPercentPerDay", native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="speed_limit", field="speedLimitKmh", device_class=SensorDeviceClass.SPEED, native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR),
    Desc(key="charge_rate", field="chargeRateKmh", device_class=SensorDeviceClass.SPEED, native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR, state_class=SensorStateClass.MEASUREMENT),
    Desc(key="soc_at_arrival", field="socAtArrival", native_unit_of_measurement=PERCENTAGE),
    Desc(key="traffic_delay", field="trafficDelayMin", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement=UnitOfTime.MINUTES),
    Desc(key="homelink_device_count", field="homelinkDeviceCount", state_class=SensorStateClass.MEASUREMENT),
    Desc(key="center_display", field="centerDisplay"),
    Desc(key="software_update_version", field="softwareUpdateVersion"),
    Desc(key="software_update_download_percent", field="softwareUpdateDownloadPercent", native_unit_of_measurement=PERCENTAGE),
    Desc(key="software_update_install_percent", field="softwareUpdateInstallPercent", native_unit_of_measurement=PERCENTAGE),
    Desc(key="software_update_duration", field="softwareUpdateDurationMin", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement=UnitOfTime.MINUTES),
    Desc(key="seat_cooler_driver", field="seatCoolerDriver", state_class=SensorStateClass.MEASUREMENT),
    Desc(key="seat_cooler_passenger", field="seatCoolerPassenger", state_class=SensorStateClass.MEASUREMENT),
]
TIRES = [("tire_fl", "frontLeft"), ("tire_fr", "frontRight"), ("tire_rl", "rearLeft"), ("tire_rr", "rearRight")]

ENERGY_SENSORS = [
    ("percentage_charged", "percentageCharged", SensorDeviceClass.BATTERY, PERCENTAGE, SensorStateClass.MEASUREMENT),
    ("solar_power", "solarPowerW", SensorDeviceClass.POWER, UnitOfPower.WATT, SensorStateClass.MEASUREMENT),
    ("battery_power", "batteryPowerW", SensorDeviceClass.POWER, UnitOfPower.WATT, SensorStateClass.MEASUREMENT),
    ("load_power", "loadPowerW", SensorDeviceClass.POWER, UnitOfPower.WATT, SensorStateClass.MEASUREMENT),
    ("grid_power", "gridPowerW", SensorDeviceClass.POWER, UnitOfPower.WATT, SensorStateClass.MEASUREMENT),
    ("generator_power", "generatorPowerW", SensorDeviceClass.POWER, UnitOfPower.WATT, SensorStateClass.MEASUREMENT),
    ("energy_left", "energyLeftWh", SensorDeviceClass.ENERGY, UnitOfEnergy.WATT_HOUR, SensorStateClass.MEASUREMENT),
    ("total_pack_energy", "totalPackEnergyWh", SensorDeviceClass.ENERGY, UnitOfEnergy.WATT_HOUR, SensorStateClass.MEASUREMENT),
    ("island_status", "islandStatus", None, None, None),
    ("grid_status", "gridStatus", None, None, None),
]


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        ents += [TCockpitSensor(c, v["vin"], d) for d in SENSORS]
        ents += [TireSensor(c, v["vin"], k, f) for k, f in TIRES]
    energy = c.energy or {}
    for site in energy.get("sites") or []:
        sid = str(site.get("id") or "")
        sname = site.get("name") or "Energy Site"
        for key, field, dc, unit, sc in ENERGY_SENSORS:
            ents.append(EnergySensor(c, sid, key, field, sname, dc, unit, sc))
        for wc in site.get("wallConnectors") or []:
            din = str(wc.get("din") or "")
            wname = wc.get("name") or "Wall Connector"
            ents.append(WallPowerSensor(c, sid, din, wname))
            ents.append(WallStateSensor(c, sid, din, wname))
            ents.append(WallVinSensor(c, sid, din, wname))
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
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, vin, key, field) -> None:
        super().__init__(coordinator, vin, key)
        self._field = field

    @property
    def native_value(self):
        return (self.state_data.get("tirePressureBar") or {}).get(self._field)


class EnergySensor(TCockpitEnergyEntity, SensorEntity):
    def __init__(self, coordinator, site_id, key, field, name, dc, unit, sc) -> None:
        super().__init__(coordinator, site_id, key, name)
        self._field = field
        self._attr_device_class = dc
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = sc

    @property
    def native_value(self):
        return self.site.get(self._field)


class WallPowerSensor(TCockpitWallConnectorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, site_id, din, name) -> None:
        super().__init__(coordinator, site_id, din, "wall_connector_power", name)

    @property
    def native_value(self):
        return self.connector.get("powerW")


class WallStateSensor(TCockpitWallConnectorEntity, SensorEntity):
    def __init__(self, coordinator, site_id, din, name) -> None:
        super().__init__(coordinator, site_id, din, "wall_connector_state", name)

    @property
    def native_value(self):
        return self.connector.get("state")


class WallVinSensor(TCockpitWallConnectorEntity, SensorEntity):
    def __init__(self, coordinator, site_id, din, name) -> None:
        super().__init__(coordinator, site_id, din, "vin", name)

    @property
    def native_value(self):
        return self.connector.get("vin")
