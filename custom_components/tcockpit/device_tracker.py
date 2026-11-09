"""Location of each vehicle (last known; reading never wakes the car)."""
from __future__ import annotations

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from .const import DOMAIN
from .entity import TCockpitEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(Location(c, v["vin"], "location") for v in c.vehicles)


class Location(TCockpitEntity, TrackerEntity):
    @property
    def source_type(self):
        return SourceType.GPS

    @property
    def latitude(self):
        return self.state_data.get("latitude")

    @property
    def longitude(self):
        return self.state_data.get("longitude")

    @property
    def extra_state_attributes(self):
        d = self.state_data
        return {"heading": d.get("heading"), "speed_kmh": d.get("speedKmh"), "address": d.get("address"), "last_seen": d.get("lastSeenAt")}
