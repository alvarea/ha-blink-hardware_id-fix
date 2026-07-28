# Blink integration — hardware_id fix (unofficial)

Minimal patch on top of the official Home Assistant Core `blink` integration
(based on version **2026.7.4**) that fixes the authentication failure
("Invalid authentication" / OAuth login rejected with `406 Not Acceptable`)
caused by Blink's servers now requiring `hardware_id` to be a UUID, while
Home Assistant still sends the literal string `"Home Assistant"`.

## What changes

One real change, in `custom_components/blink/const.py`:

```diff
- HARDWARE_ID = "Home Assistant"
+ HARDWARE_ID = "a1b2c3d4-e5f6-47a8-9b12-abcdef123456"
```

Everything else is identical to the official HA 2026.7.4 code. A
`"version"` field was also added to `manifest.json`, which HACS requires
for custom integrations.

## Symptoms this fixes

- Adding/re-authenticating the Blink integration fails immediately with
  **"Invalid authentication"**, without ever reaching the 2FA PIN step
- Debug logs (`blinkpy: debug`) show a `406 Not Acceptable` response from
  Blink's OAuth endpoint (`api.oauth.blink.com/oauth/v2/authorize`)
- The Blink mobile app logs in fine with the same credentials — confirming
  it's not a credentials or account issue, but something specific to how
  Home Assistant identifies itself to Blink's servers

## Root cause

Blink's OAuth server started rejecting any `hardware_id` value that isn't
formatted as a UUID. Home Assistant's `blink` integration hardcodes
`HARDWARE_ID = "Home Assistant"` (a plain string), which the server now
rejects outright with a 406, before authentication even gets a chance to
happen. This explains why the failure looks like invalid credentials even
though the credentials are correct.

## Bug references

- https://github.com/home-assistant/core/issues/158760
- https://github.com/home-assistant/core/issues/173520
- https://github.com/home-assistant/core/issues/176708
- https://community.home-assistant.io/t/blink-integration-broken-after-ha-restart-cannot-complete-2fa-pin-entry-eu-uk-sms-2fa/1013424/17

## Installation (via HACS)

1. In HACS → menu (⋮) → **Custom repositories**
2. Add this repository's URL, category **Integration**
3. Install "Blink (hardware_id fix)"
4. Restart Home Assistant
5. Go to your existing Blink integration and click **Reauthenticate** (or
   remove it and add it again from scratch)

You should now be prompted for the 2FA PIN instead of getting an immediate
"Invalid authentication" error.

## ⚠️ Important notes

- This **replaces** the official `blink` integration while installed via
  `custom_components/blink` (Home Assistant prioritizes
  `custom_components` over built-in integrations with the same domain).
- When Home Assistant eventually ships an official fix, you should
  **remove this custom repository from HACS** to go back to the official
  integration — otherwise you'll stay "frozen" on this patched version and
  won't get further official updates to Blink.
- Not officially maintained by Home Assistant or by Anthropic — it's a
  one-line manual patch, produced after diagnosing the issue with the help
  of Claude (Anthropic).

## Contributing / staying in sync

This repo is a straight copy of `homeassistant/components/blink` from HA
Core, with the one-line change above. If you want to rebase it onto a
newer HA Core version yourself, just diff `const.py` against the upstream
file for your version and reapply the same change.

Issues and PRs welcome — especially if Blink changes their API again, or
if you find a cleaner way to make `hardware_id` configurable without a
full integration copy.
