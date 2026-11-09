"""Base entity: one device per vehicle or energy site / wall connector."""
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
        if hasattr(self.coordinator, "vehicle_state"):
            return self.coordinator.vehicle_state(self.vin)
        # Back-compat if data is still a flat vin map
        data = self.coordinator.data or {}
        if "vehicles" in data:
            return (data.get("vehicles") or {}).get(self.vin) or {}
        return data.get(self.vin) or {}

    @property
    def available(self) -> bool:
        return super().available and bool(self.state_data)


class TCockpitEnergyEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, site_id: str, key: str, name: str, model: str = "Energy Site") -> None:
        super().__init__(coordinator)
        self.site_id = str(site_id)
        self._attr_unique_id = f"{self.site_id}-{key}"
        self._attr_translation_key = key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"energy_{self.site_id}")},
            name=name or "Energy Site",
            manufacturer="Tesla (via TCockpit)",
            model=model,
        )

    @property
    def site(self) -> dict:
        energy = (self.coordinator.data or {}).get("energy") or self.coordinator.energy or {}
        for s in energy.get("sites") or []:
            if str(s.get("id")) == self.site_id:
                return s
        return {}

    @property
    def available(self) -> bool:
        return super().available and bool(self.site)


class TCockpitWallConnectorEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, site_id: str, din: str, key: str, name: str) -> None:
        super().__init__(coordinator)
        self.site_id = str(site_id)
        self.din = str(din)
        self._attr_unique_id = f"{self.site_id}-{self.din}-{key}"
        self._attr_translation_key = key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"wc_{self.din or self.site_id}")},
            name=name or "Wall Connector",
            manufacturer="Tesla (via TCockpit)",
            model="Wall Connector",
            via_device=(DOMAIN, f"energy_{self.site_id}"),
        )

    @property
    def connector(self) -> dict:
        energy = (self.coordinator.data or {}).get("energy") or self.coordinator.energy or {}
        for s in energy.get("sites") or []:
            if str(s.get("id")) != self.site_id:
                continue
            for wc in s.get("wallConnectors") or []:
                if str(wc.get("din")) == self.din:
                    return wc
        return {}

    @property
    def available(self) -> bool:
        return super().available and bool(self.connector)
