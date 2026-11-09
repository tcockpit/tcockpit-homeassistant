"""Software version + optional schedule_software_update install."""
from __future__ import annotations

from homeassistant.components.update import UpdateEntity, UpdateEntityFeature

from .const import DOMAIN
from .entity import TCockpitEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(SoftwareUpdate(c, v["vin"]) for v in c.vehicles)


class SoftwareUpdate(TCockpitEntity, UpdateEntity):
    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "update")
        feats = UpdateEntityFeature(0)
        if coordinator.can("schedule_software_update"):
            feats |= UpdateEntityFeature.INSTALL
        self._attr_supported_features = feats

    @property
    def installed_version(self):
        return self.state_data.get("softwareVersion")

    @property
    def latest_version(self):
        avail = self.state_data.get("softwareUpdateVersion")
        if self.state_data.get("softwareUpdateAvailable") and avail:
            return avail
        return self.state_data.get("softwareVersion")

    @property
    def title(self):
        return "Tesla Software"

    @property
    def in_progress(self):
        return bool(self.state_data.get("softwareUpdateInProgress")) or None

    @property
    def release_summary(self):
        dur = self.state_data.get("softwareUpdateDurationMin")
        if dur is not None:
            return f"Expected duration ~{dur} min"
        return None

    async def async_install(self, version: str | None, backup: bool, **kwargs) -> None:
        # offset_sec=0 → install as soon as ready
        await self.coordinator.api.command(self.vin, "schedule_software_update", offset_sec=0)
        await self.coordinator.async_request_refresh()
