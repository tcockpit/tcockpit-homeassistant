"""Binary sensors: charging, plugged-in port, doors/windows/trunks open, sentry."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity

from .const import DOMAIN
from .entity import TCockpitEntity

ITEMS = [
    ("charging", "charging", BinarySensorDeviceClass.BATTERY_CHARGING),
    ("charge_port_open", "chargePortOpen", BinarySensorDeviceClass.OPENING),
    ("doors_open", "doorsOpen", BinarySensorDeviceClass.DOOR),
    ("windows_open", "windowsOpen", BinarySensorDeviceClass.WINDOW),
    ("trunk_open", "trunkOpen", BinarySensorDeviceClass.OPENING),
    ("frunk_open", "frunkOpen", BinarySensorDeviceClass.OPENING),
    ("sentry_mode", "sentryMode", None),
    ("climate_on", "climateOn", None),
]


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(Flag(c, v["vin"], k, f, d) for v in c.vehicles for k, f, d in ITEMS)


class Flag(TCockpitEntity, BinarySensorEntity):
    def __init__(self, coordinator, vin, key, field, device_class) -> None:
        super().__init__(coordinator, vin, key)
        self._field = field
        self._attr_device_class = device_class

    @property
    def is_on(self):
        value = self.state_data.get(self._field)
        return None if value is None else bool(value)
