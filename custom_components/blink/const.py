"""Constants for Blink."""

from hashlib import sha256
from uuid import UUID

from homeassistant.const import Platform

DOMAIN = "blink"
# Blink's OAuth server rejects non-UUID hardware_id values with HTTP 406
# Not Acceptable. The upstream string "Home Assistant" no longer works.
# Bug references: home-assistant/core#158760, #173520, #176708, #177284


def hardware_id_from_email(email: str) -> str:
    """Return a stable UUIDv4-formatted hardware ID for an email address.

    UUIDv4 values are normally random. This intentionally derives the UUID
    bytes from the normalized email address so the same Blink account keeps
    the same hardware ID across restarts and reauthentication. UUID version
    and variant bits are set explicitly to satisfy services that validate the
    UUIDv4 format.
    """
    normalized_email = email.strip().casefold()
    digest = sha256(f"blink-hardware-id:{normalized_email}".encode()).digest()
    return str(UUID(bytes=digest[:16], version=4))

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
