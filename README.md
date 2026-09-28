*[Leer en español](README_ES.md)*

# Blink integration — hardware_id fix (unofficial)

Minimal patch on top of the official Home Assistant Core `blink` integration
(rebased on version **2026.8.2**, blinkpy `0.25.9`) that fixes the
authentication failure ("Invalid authentication" / OAuth login rejected
with `406 Not Acceptable`) caused by Blink's servers now requiring
`hardware_id` to be a UUID, while Home Assistant still sends the literal
string `"Home Assistant"`.

The integration automatically creates a UUIDv4-formatted `hardware_id` from
the email address entered during setup, saves it in Home Assistant, and
reuses it thereafter. No manual UUID generation or source edits are required.

## Symptoms this fixes

- Adding/re-authenticating the Blink integration fails immediately with
  **"Invalid authentication"**, without ever reaching the 2FA PIN step
- Debug logs (`blinkpy: debug`) show a `406 Not Acceptable` response from
  Blink's OAuth endpoint (`api.oauth.blink.com/oauth/v2/authorize`)
- Arming/disarming the alarm, or refreshing camera images, fails with
  `TokenRefreshFailed` / `LoginError` once the access token expires —
  this was traced to `blinkpy 0.25.6`'s legacy re-login path reading a
  `device_id` field that HA never sets (defaults to `"Blinkpy"`, also
  rejected by Blink). Bumping to `blinkpy 0.25.9` removes that legacy
  code path entirely, using `hardware_id` consistently instead.
- The Blink mobile app logs in fine with the same credentials — confirming
  it's not a credentials or account issue

## Root cause

Blink's OAuth server started rejecting any `hardware_id` value that isn't
formatted as a UUID. Home Assistant's `blink` integration hardcodes
`HARDWARE_ID = "Home Assistant"` (a plain string), which the server now
rejects outright with a 406, before authentication even gets a chance to
happen.

## Bug references

- https://github.com/home-assistant/core/issues/158760
- https://github.com/home-assistant/core/issues/173520
- https://github.com/home-assistant/core/issues/176708
- https://github.com/home-assistant/core/issues/177284
- https://community.home-assistant.io/t/blink-integration-broken-after-ha-restart-cannot-complete-2fa-pin-entry-eu-uk-sms-2fa/1013424/17

## Installation (via HACS)

1. In HACS → menu (⋮) → **Custom repositories**
2. Add this repository's URL, category **Integration**
3. Install "Blink (hardware_id fix)"
4. Restart Home Assistant
5. If an existing Blink integration needs to be authenticated again, click
   **Reauthenticate** (or remove it and add it again from scratch)

You should now be prompted for the 2FA PIN instead of getting an immediate
"Invalid authentication" error, and arm/disarm actions should stop failing
with `TokenRefreshFailed`.

## ⚠️ Important notes

- This **replaces** the official `blink` integration while installed via
  `custom_components/blink` (Home Assistant prioritizes
  `custom_components` over built-in integrations with the same domain).
- When Home Assistant eventually ships an official fix, you should
  **remove this custom repository from HACS** to go back to the official
  integration.
- Not officially maintained by Home Assistant or by Anthropic — it's a
  small manual patch, produced after diagnosing the issue with the help
  of Claude (Anthropic).

## Contributing / staying in sync

This repo is a copy of `homeassistant/components/blink` from HA Core
2026.8.2, with the changes above. If you want to rebase it onto a newer
HA Core version yourself, diff `const.py` and `manifest.json` against the
upstream files for your version and reapply the same changes.

Issues and PRs welcome.
