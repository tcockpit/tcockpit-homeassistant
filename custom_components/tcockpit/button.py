"""One-shot actions: trunk/frunk, charge port, windows, honk/flash, wake, media."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity

from .const import DOMAIN
from .entity import TCockpitEntity

# (unique_key, command)
ITEMS = [
    ("trunk", "trunk"),
    ("frunk", "frunk"),
    ("open_charge_port", "open_charge_port"),
    ("close_charge_port", "close_charge_port"),
    ("vent_windows", "vent_windows"),
    ("close_windows", "close_windows"),
    ("honk", "honk"),
    ("flash_lights", "flash_lights"),
    ("wake_up", "wake_up"),
    ("media_toggle_playback", "media_toggle_playback"),
    ("media_next_track", "media_next_track"),
    ("media_prev_track", "media_prev_track"),
    ("media_volume_up", "media_volume_up"),
    ("media_volume_down", "media_volume_down"),
    ("homelink", "homelink"),
    ("boombox", "boombox"),
]


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        for key, cmd in ITEMS:
            if c.can(cmd):
                ents.append(Action(c, v["vin"], key, cmd))
    async_add_entities(ents)


class Action(TCockpitEntity, ButtonEntity):
    def __init__(self, coordinator, vin, key, command) -> None:
        super().__init__(coordinator, vin, key)
        self._command = command

    async def async_press(self) -> None:
        await self.coordinator.api.command(self.vin, self._command)
        await self.coordinator.async_request_refresh()
