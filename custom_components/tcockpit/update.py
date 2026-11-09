"""Software version as an Update entity (install not supported — Fleet schedule_software_update not wired)."""
from __future__ import annotations

from homeassistant.components.update import UpdateEntity, UpdateEntityFeature

from .const import DOMAIN
from .entity import TCockpitEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(SoftwareUpdate(c, v["vin"]) for v in c.vehicles)


class SoftwareUpdate(TCockpitEntity, UpdateEntity):
    _attr_supported_features = UpdateEntityFeature(0)  # display only

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "update")

    @property
    def installed_version(self):
        return self.state_data.get("softwareVersion")

    @property
    def latest_version(self):
        # Without a separate "update available" stream, mirror installed
        return self.state_data.get("softwareVersion")

    @property
    def title(self):
        return "Tesla Software"
