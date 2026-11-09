"""Base entity: one device per vehicle."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER


class TCockpitEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, vin: str, key: str) -> None:
        super().__init__(coordinator)
        self.vin = vin
        self._attr_unique_id = f"{vin}_{key}"
        self._attr_translation_key = key
        meta = next((v for v in coordinator.vehicles if v["vin"] == vin), {})
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, vin)}, name=meta.get("name") or "Tesla",
            manufacturer=MANUFACTURER, model=meta.get("model") or "Tesla",
        )

    @property
    def state_data(self) -> dict:
        return (self.coordinator.data or {}).get(self.vin) or {}

    @property
    def available(self) -> bool:
        return super().available and bool(self.state_data)
