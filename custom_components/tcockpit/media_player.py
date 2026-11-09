"""Media player wrapping the same media commands as the app (no track metadata from Fleet Telemetry)."""
from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)

from .const import DOMAIN
from .entity import TCockpitEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        if c.can("media_toggle_playback"):
            ents.append(VehicleMedia(c, v["vin"]))
    async_add_entities(ents)


class VehicleMedia(TCockpitEntity, MediaPlayerEntity):
    _attr_supported_features = (
        MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.NEXT_TRACK
        | MediaPlayerEntityFeature.PREVIOUS_TRACK
        | MediaPlayerEntityFeature.VOLUME_STEP
    )

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "mediaplayer")

    @property
    def state(self):
        # Fleet Telemetry does not stream play/pause reliably → idle when online else off
        if self.state_data.get("online") is False:
            return MediaPlayerState.OFF
        return MediaPlayerState.IDLE

    async def async_media_play(self) -> None:
        await self.coordinator.api.command(self.vin, "media_toggle_playback")

    async def async_media_pause(self) -> None:
        await self.coordinator.api.command(self.vin, "media_toggle_playback")

    async def async_media_next_track(self) -> None:
        await self.coordinator.api.command(self.vin, "media_next_track")

    async def async_media_previous_track(self) -> None:
        await self.coordinator.api.command(self.vin, "media_prev_track")

    async def async_volume_up(self) -> None:
        await self.coordinator.api.command(self.vin, "media_volume_up")

    async def async_volume_down(self) -> None:
        await self.coordinator.api.command(self.vin, "media_volume_down")
