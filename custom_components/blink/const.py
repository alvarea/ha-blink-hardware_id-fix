"""Constants for Blink."""

from homeassistant.const import Platform

DOMAIN = "blink"
# PATCH (alvarea): Blink's OAuth server rejects non-UUID hardware_id values
# with HTTP 406 Not Acceptable. The upstream string "Home Assistant" no
# longer works. Using a fixed, private UUID here (instead of a random one,
# and instead of a publicly shared one) keeps the value stable across
# restarts/reauth, which blinkpy needs for token persistence, without
# colliding with other users' identities on Blink's servers.
# See: home-assistant/core#158760, #173520, #176708, #177284
HARDWARE_ID = "7d6596ff-a5f5-43c5-9ecb-a4fd9ed373e1"

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
