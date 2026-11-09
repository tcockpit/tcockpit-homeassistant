"""Door lock. Locking needs a key with control; unlocking additionally needs 'Entriegeln erlauben'."""
from __future__ import annotations

from homeassistant.components.lock import LockEntity
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .entity import TCockpitEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    if not c.can("lock"):
        return
    async_add_entities(DoorLock(c, v["vin"], "door_lock") for v in c.vehicles)


class DoorLock(TCockpitEntity, LockEntity):
    @property
    def is_locked(self):
        value = self.state_data.get("locked")
        return None if value is None else bool(value)

    async def async_lock(self, **kwargs) -> None:
        await self.coordinator.api.command(self.vin, "lock")
        await self.coordinator.async_request_refresh()

    async def async_unlock(self, **kwargs) -> None:
        if not self.coordinator.can("unlock"):
            raise HomeAssistantError("Dieser TCockpit-Schlüssel darf nicht entriegeln / this key may not unlock.")
        await self.coordinator.api.command(self.vin, "unlock")
        await self.coordinator.async_request_refresh()
