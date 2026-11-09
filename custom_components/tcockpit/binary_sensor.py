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


class EnergyFlag(TCockpitEnergyEntity, BinarySensorEntity):
    def __init__(self, coordinator, site_id, key, field, name, device_class) -> None:
        super().__init__(coordinator, site_id, key, name)
        self._field = field
        self._attr_device_class = device_class

    @property
    def is_on(self):
        value = self.site.get(self._field)
        return None if value is None else bool(value)
