"""Binary sensors: online, charging, doors/windows (aggregate + per-side), energy flags."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity

from .const import DOMAIN
from .entity import TCockpitEntity, TCockpitEnergyEntity

ITEMS = [
    ("online", "online", BinarySensorDeviceClass.CONNECTIVITY),  # Tessie: status
    ("charging", "charging", BinarySensorDeviceClass.BATTERY_CHARGING),
    ("charge_port_open", "chargePortOpen", BinarySensorDeviceClass.OPENING),
    ("charge_port_latched", "chargePortLatched", None),
    ("doors_open", "doorsOpen", BinarySensorDeviceClass.DOOR),
    ("windows_open", "windowsOpen", BinarySensorDeviceClass.WINDOW),
    ("trunk_open", "trunkOpen", BinarySensorDeviceClass.OPENING),
    ("frunk_open", "frunkOpen", BinarySensorDeviceClass.OPENING),
    ("sentry_mode", "sentryMode", None),
    ("climate_on", "climateOn", None),
    ("preconditioning", "preconditioning", None),
    ("cabin_overheat_protection", "cabinOverheatProtection", None),
    # v0.4.0
    ("battery_heater", "batteryHeaterOn", None),
    ("driver_present", "driverPresent", BinarySensorDeviceClass.OCCUPANCY),
    ("valet_mode", "valetMode", None),
    ("guest_mode", "guestMode", None),
    ("auto_seat_climate_left", "autoSeatClimateLeft", None),
    ("auto_seat_climate_right", "autoSeatClimateRight", None),
    ("auto_steering_wheel_heat", "autoSteeringWheelHeat", None),
    ("seat_vent", "seatVentEnabled", None),
    ("homelink_nearby", "homelinkNearby", None),
    ("speed_limit_mode", "speedLimitMode", None),
    ("software_update_available", "softwareUpdateAvailable", BinarySensorDeviceClass.UPDATE),
    ("software_update_in_progress", "softwareUpdateInProgress", None),
    ("scheduled_charging_pending", "scheduledChargingPending", None),
]

# Per-door / per-window (Tessie parity)
DOOR_KEYS = [
    ("driver_front_door", "driverFront", BinarySensorDeviceClass.DOOR),
    ("passenger_front_door", "passengerFront", BinarySensorDeviceClass.DOOR),
    ("driver_rear_door", "driverRear", BinarySensorDeviceClass.DOOR),
    ("passenger_rear_door", "passengerRear", BinarySensorDeviceClass.DOOR),
]
WINDOW_KEYS = [
    ("front_driver_window", "frontDriver", BinarySensorDeviceClass.WINDOW),
    ("front_passenger_window", "frontPassenger", BinarySensorDeviceClass.WINDOW),
    ("rear_driver_window", "rearDriver", BinarySensorDeviceClass.WINDOW),
    ("rear_passenger_window", "rearPassenger", BinarySensorDeviceClass.WINDOW),
]

# TPMS soft/hard warnings per corner (server fields tpmsSoft / tpmsHard)
TPMS_WARN = [
    ("tpms_soft_fl", "soft", "frontLeft"),
    ("tpms_soft_fr", "soft", "frontRight"),
    ("tpms_soft_rl", "soft", "rearLeft"),
    ("tpms_soft_rr", "soft", "rearRight"),
    ("tpms_hard_fl", "hard", "frontLeft"),
    ("tpms_hard_fr", "hard", "frontRight"),
    ("tpms_hard_rl", "hard", "rearLeft"),
    ("tpms_hard_rr", "hard", "rearRight"),
]

ENERGY_FLAGS = [
    ("backup_capable", "backupCapable", None),
    ("grid_services_active", "gridServicesActive", None),
    ("grid_services_enabled", "gridServicesEnabled", None),
    ("storm_mode_active", "stormModeActive", None),
    ("grid_status_active", "gridStatusActive", BinarySensorDeviceClass.POWER),
]


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        vin = v["vin"]
        ents += [Flag(c, vin, k, f, d) for k, f, d in ITEMS]
        ents += [DoorFlag(c, vin, k, f, d) for k, f, d in DOOR_KEYS]
        ents += [WindowFlag(c, vin, k, f, d) for k, f, d in WINDOW_KEYS]
        ents += [TpmsWarn(c, vin, k, kind, corner) for k, kind, corner in TPMS_WARN]
    for site in (c.energy or {}).get("sites") or []:
        sid = str(site.get("id") or "")
        sname = site.get("name") or "Energy Site"
        for key, field, dc in ENERGY_FLAGS:
            ents.append(EnergyFlag(c, sid, key, field, sname, dc))
    async_add_entities(ents)


class Flag(TCockpitEntity, BinarySensorEntity):
    def __init__(self, coordinator, vin, key, field, device_class) -> None:
        super().__init__(coordinator, vin, key)
        self._field = field
        self._attr_device_class = device_class

    @property
    def is_on(self):
        value = self.state_data.get(self._field)
        return None if value is None else bool(value)


class DoorFlag(TCockpitEntity, BinarySensorEntity):
    def __init__(self, coordinator, vin, key, field, device_class) -> None:
        super().__init__(coordinator, vin, key)
        self._field = field
        self._attr_device_class = device_class

    @property
    def is_on(self):
        doors = self.state_data.get("doors") or {}
        value = doors.get(self._field)
        return None if value is None else bool(value)


class WindowFlag(TCockpitEntity, BinarySensorEntity):
    def __init__(self, coordinator, vin, key, field, device_class) -> None:
        super().__init__(coordinator, vin, key)
        self._field = field
        self._attr_device_class = device_class

    @property
    def is_on(self):
        wins = self.state_data.get("windows") or {}
        value = wins.get(self._field)
        return None if value is None else bool(value)



class TpmsWarn(TCockpitEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    def __init__(self, coordinator, vin, key, kind, corner) -> None:
        super().__init__(coordinator, vin, key)
        self._kind, self._corner = kind, corner

    @property
    def is_on(self):
        bag = self.state_data.get("tpmsSoft" if self._kind == "soft" else "tpmsHard") or {}
        value = bag.get(self._corner)
        return None if value is None else bool(value)


class EnergyFlag(TCockpitEnergyEntity, BinarySensorEntity):
    def __init__(self, coordinator, site_id, key, field, name, device_class) -> None:
        super().__init__(coordinator, site_id, key, name)
        self._field = field
        self._attr_device_class = device_class

    @property
    def is_on(self):
        value = self.site.get(self._field)
        return None if value is None else bool(value)
