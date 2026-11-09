"""Selects: climate keeper mode and seat heater levels."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity

from .const import DOMAIN
from .entity import TCockpitEntity

KEEPER_OPTIONS = ["off", "hold", "dog", "camp"]
HEAT_OPTIONS = ["0", "1", "2", "3"]  # off … max
# (unique_key, state_field, seat_index) — seat index matches server seat_heater
SEATS = [
    ("seat_heater_driver", "driverSeatHeat", 0),
    ("seat_heater_passenger", "passengerSeatHeat", 1),
    ("seat_heater_rear_left", "rearLeftSeatHeat", 2),
    ("seat_heater_rear_center", "rearCenterSeatHeat", 3),
    ("seat_heater_rear_right", "rearRightSeatHeat", 4),
]
COOL_OPTIONS = ["0", "1", "2", "3"]
COOLERS = [
    ("seat_cooler_driver", "seatCoolerDriver", 0),
    ("seat_cooler_passenger", "seatCoolerPassenger", 1),
]


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = []
    for v in c.vehicles:
        if c.can("climate_keeper"):
            ents.append(ClimateKeeper(c, v["vin"]))
        if c.can("seat_heater"):
            ents += [SeatHeater(c, v["vin"], key, field, seat) for key, field, seat in SEATS]
        if c.can("seat_cooler"):
            ents += [SeatCooler(c, v["vin"], key, field, seat) for key, field, seat in COOLERS]
    async_add_entities(ents)


class ClimateKeeper(TCockpitEntity, SelectEntity):
    _attr_options = KEEPER_OPTIONS

    def __init__(self, coordinator, vin) -> None:
        super().__init__(coordinator, vin, "climate_keeper")

    @property
    def current_option(self):
        value = self.state_data.get("climateKeeper")
        if value in KEEPER_OPTIONS:
            return value
        return None

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.api.command(self.vin, "climate_keeper", mode=option)
        await self.coordinator.async_request_refresh()


class SeatHeater(TCockpitEntity, SelectEntity):
    _attr_options = HEAT_OPTIONS

    def __init__(self, coordinator, vin, key, field, seat) -> None:
        super().__init__(coordinator, vin, key)
        self._field = field
        self._seat = seat

    @property
    def current_option(self):
        value = self.state_data.get(self._field)
        if value is None:
            return None
        level = max(0, min(3, int(value)))
        return str(level)

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.api.command(self.vin, "seat_heater", seat=self._seat, level=int(option))
        await self.coordinator.async_request_refresh()


class SeatCooler(TCockpitEntity, SelectEntity):
    _attr_options = COOL_OPTIONS

    def __init__(self, coordinator, vin, key, field, seat) -> None:
        super().__init__(coordinator, vin, key)
        self._field = field
        self._seat = seat

    @property
    def current_option(self):
        value = self.state_data.get(self._field)
        if value is None:
            return None
        level = max(0, min(3, int(value)))
        return str(level)

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.api.command(self.vin, "seat_cooler", seat=self._seat, level=int(option))
        await self.coordinator.async_request_refresh()
