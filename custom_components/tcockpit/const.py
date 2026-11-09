"""Constants for the TCockpit integration."""
DOMAIN = "tcockpit"
DEFAULT_URL = "https://tcockpit.de"
CONF_API_KEY = "api_key"
CONF_URL = "url"
SCAN_INTERVAL_SECONDS = 60  # reading never wakes the car
MANUFACTURER = "Tesla (via TCockpit)"

# Fleet API wall_connector_state — same IntEnum as HA core tessie.const.TessieWallConnectorStates
# (verified against home-assistant/core .../tessie/const.py). Local tesla_wall_connector LAN codes differ.
WALL_CONNECTOR_STATES = {
    0: "booting",
    1: "charging",
    2: "disconnected",
    4: "connected",
    5: "scheduled",
    6: "negotiating",
    7: "error",
    8: "charging_finished",
    9: "waiting_car",
    10: "charging_reduced",
}

