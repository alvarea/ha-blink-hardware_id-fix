*[Leer en español](README_ES.md)*

# Blink integration — hardware_id fix (unofficial)

Minimal patch on top of the official Home Assistant Core `blink` integration
(rebased on version **2026.8.2**, blinkpy `0.25.9`) that fixes the
authentication failure ("Invalid authentication" / OAuth login rejected
with `406 Not Acceptable`) caused by Blink's servers now requiring
`hardware_id` to be a UUID, while Home Assistant still sends the literal
string `"Home Assistant"`.

## ⚠️ Before installing: generate YOUR OWN UUID

**Do not use the placeholder UUID that ships in this repo's `const.py`.**
Each installation needs its own private, unique `hardware_id`. Reusing the
same value across different Blink accounts/installations can cause Blink's
anti-fraud systems to flag or block that value — which is exactly what
happened to the original author after this fix got shared in the Home
Assistant community forum with a real, working UUID baked into the code.
Authentication broke again for everyone using the shared value.

**Generate your own before installing:**

```bash
# macOS / Linux
uuidgen

# Python (any OS)
python3 -c "import uuid; print(uuid.uuid4())"
```

Then edit `custom_components/blink/const.py` and replace the
`HARDWARE_ID` placeholder with your own generated value, **before**
adding this as a HACS custom repository / before your first download.

If you already installed an earlier version of this fix using the shared
UUID, generate a new private one and update your local `const.py`, then
push the change to your own fork/copy of this repo and update via HACS.

## What changes

One real change, in `custom_components/blink/const.py`:

```diff
- HARDWARE_ID = "Home Assistant"
+ HARDWARE_ID = "<your-own-private-uuid>"
```

Everything else is identical to the official HA 2026.8.2 code. A
`"version"` field was also added to `manifest.json`, which HACS requires
for custom integrations, and `blinkpy` is pinned to `0.25.9` (matching
HA 2026.8.x), which also resolves a separate `TokenRefreshFailed` bug
affecting arm/disarm and camera image refresh (see below).

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

1. Generate your own private UUID (see above) and edit
   `custom_components/blink/const.py` in your own copy/fork of this repo
2. In HACS → menu (⋮) → **Custom repositories**
3. Add this repository's URL, category **Integration**
4. Install "Blink (hardware_id fix)"
5. Restart Home Assistant
6. Go to your existing Blink integration and click **Reauthenticate** (or
   remove it and add it again from scratch) — this is expected: changing
   `hardware_id` invalidates any previous session, so you'll need to pass
   the 2FA step again once

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
upstream files for your version and reapply the same changes (remembering
to use your own private UUID, not a shared one).

Issues and PRs welcome.
