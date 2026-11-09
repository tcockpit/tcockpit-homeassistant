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
            manufacturer=MANUFACTURER,
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


def _wc_serial(din: str, connector: dict | None = None) -> str | None:
    """Serial like Tessie: last DIN segment, else API serialNumber."""
    if connector:
        sn = connector.get("serialNumber") or connector.get("serial")
        if sn:
            return str(sn)
    if not din:
        return None
    return din.rsplit("-", maxsplit=1)[-1] or None


def _wc_model(connector: dict | None = None) -> str:
    if not connector:
        return "Wall Connector"
    model = connector.get("model") or connector.get("partName")
    if model:
        # Normalize "Gen 3 Wall Connector" → "Wall Connector Gen 3"
        m = str(model)
        if m.lower().startswith("gen ") and "wall connector" in m.lower():
            # "Gen 3 Wall Connector" → "Wall Connector Gen 3"
            parts = m.split()
            if len(parts) >= 3 and parts[0].lower() == "gen":
                return f"Wall Connector Gen {parts[1]}"
        return m
    evse = str(connector.get("evseType") or "")
    if "gen_3" in evse:
        return "Wall Connector Gen 3"
    if "gen_2" in evse:
        return "Wall Connector Gen 2"
    return "Wall Connector"


class TCockpitWallConnectorEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, site_id: str, din: str, key: str, name: str) -> None:
        super().__init__(coordinator)
        self.site_id = str(site_id)
        self.din = str(din)
        self._attr_unique_id = f"{self.site_id}-{self.din}-{key}"
        self._attr_translation_key = key
        # Device name matches Tessie ("Wall Connector"); serial/model filled on first data.
        connector = {}
        energy = getattr(coordinator, "energy", None) or {}
        for s in energy.get("sites") or []:
            if str(s.get("id")) != self.site_id:
                continue
            for wc in s.get("wallConnectors") or []:
                if str(wc.get("din")) == self.din:
                    connector = wc
                    break
        serial = _wc_serial(self.din, connector)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"wc_{self.din or self.site_id}")},
            name="Wall Connector",
            manufacturer="Tesla",
            model=_wc_model(connector),
            serial_number=serial,
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
