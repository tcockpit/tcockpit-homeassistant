"""Location + navigation destination (route) trackers."""
from __future__ import annotations

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from .const import DOMAIN
from .entity import TCockpitEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        ents.append(Location(c, v["vin"], "location"))
        ents.append(Route(c, v["vin"], "route"))
    async_add_entities(ents)


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


class Route(TCockpitEntity, TrackerEntity):
    """Destination of the active nav route (Tessie device_tracker.route)."""

    @property
    def source_type(self):
        return SourceType.GPS

    @property
    def latitude(self):
        return self.state_data.get("destinationLatitude")

    @property
    def longitude(self):
        return self.state_data.get("destinationLongitude")

    @property
    def location_name(self):
        return self.state_data.get("destination")

    @property
    def extra_state_attributes(self):
        d = self.state_data
        return {
            "destination": d.get("destination"),
            "remaining_km": d.get("remainingKm"),
            "minutes_to_arrival": d.get("minutesToArrival"),
            "navigating": d.get("navigating"),
        }
