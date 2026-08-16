"""Constants for Blink."""

from homeassistant.const import Platform

DOMAIN = "blink"
# PATCH (alvarea): Blink's OAuth server rejects non-UUID hardware_id values
# with HTTP 406 Not Acceptable. The upstream string "Home Assistant" no
# longer works.
#
# ⚠️ REQUIRED: replace the placeholder below with YOUR OWN randomly
# generated UUID before installing. Do NOT reuse the same value across
# different Blink accounts/installations — Blink's servers may flag or
# block a hardware_id that's shared by many unrelated accounts, causing
# authentication to fail again for everyone using it.
#
# Generate your own:
#   macOS/Linux:  uuidgen
#   Python:       python3 -c "import uuid; print(uuid.uuid4())"
#
# See README.md for full instructions.
# Bug references: home-assistant/core#158760, #173520, #176708, #177284
HARDWARE_ID = "REPLACE-WITH-YOUR-OWN-UUID-0000-000000000000"

CONF_MIGRATE = "migrate"
CONF_CAMERA = "camera"
CONF_ALARM_CONTROL_PANEL = "alarm_control_panel"
DEFAULT_BRAND = "Blink"
DEFAULT_ATTRIBUTION = "Data provided by immedia-semi.com"
DEFAULT_SCAN_INTERVAL = 300
DEFAULT_OFFSET = 1
SIGNAL_UPDATE_BLINK = "blink_update"

TYPE_CAMERA_ARMED = "motion_enabled"
TYPE_MOTION_DETECTED = "motion_detected"
TYPE_TEMPERATURE = "temperature"
TYPE_BATTERY = "battery"
TYPE_WIFI_STRENGTH = "wifi_strength"


PLATFORMS = [
    Platform.ALARM_CONTROL_PANEL,
    Platform.BINARY_SENSOR,
    Platform.CAMERA,
    Platform.SENSOR,
    Platform.SWITCH,
]
