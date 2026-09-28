*[Read in English](README.md)*

# Blink integration — fix del hardware_id (no oficial)

Parche mínimo sobre la integración oficial `blink` de Home Assistant Core
(basado en la versión **2026.8.2**, blinkpy `0.25.9`) que corrige el fallo
de autenticación ("Invalid authentication" / login OAuth rechazado con
`406 Not Acceptable`) causado por que el servidor de Blink ahora exige
que `hardware_id` tenga formato UUID, mientras que Home Assistant sigue
enviando el string literal `"Home Assistant"`.

La integración crea automáticamente un `hardware_id` con formato UUIDv4 a
partir del email introducido durante la configuración, lo guarda en Home
Assistant y lo reutiliza posteriormente. No hace falta generar un UUID ni
editar el código.

## Síntomas que corrige

- Añadir o reautenticar la integración Blink falla inmediatamente con
  **"Invalid authentication"**, sin llegar nunca al paso del PIN de 2FA
- Los logs de debug (`blinkpy: debug`) muestran una respuesta
  `406 Not Acceptable` del endpoint OAuth de Blink
  (`api.oauth.blink.com/oauth/v2/authorize`)
- Armar/desarmar la alarma, o refrescar las imágenes de cámara, falla con
  `TokenRefreshFailed` / `LoginError` una vez caduca el token de acceso —
  esto se rastreó hasta la ruta legacy de re-login de `blinkpy 0.25.6`,
  que lee un campo `device_id` que HA nunca establece (por defecto
  `"Blinkpy"`, también rechazado por Blink). Al pasar a `blinkpy 0.25.9`
  esa ruta de código legacy desaparece por completo, usando siempre
  `hardware_id` en su lugar.
- La app móvil de Blink inicia sesión sin problema con las mismas
  credenciales — confirmando que no es un problema de cuenta/credenciales

## Causa raíz

El servidor OAuth de Blink empezó a rechazar cualquier valor de
`hardware_id` que no tenga formato UUID. La integración `blink` de Home
Assistant tiene hardcodeado `HARDWARE_ID = "Home Assistant"` (un string
plano), que el servidor ahora rechaza directamente con un 406, antes
incluso de que la autenticación tenga ocasión de completarse.

## Referencias del bug

- https://github.com/home-assistant/core/issues/158760
- https://github.com/home-assistant/core/issues/173520
- https://github.com/home-assistant/core/issues/176708
- https://github.com/home-assistant/core/issues/177284
- https://community.home-assistant.io/t/blink-integration-broken-after-ha-restart-cannot-complete-2fa-pin-entry-eu-uk-sms-2fa/1013424/17

## Instalación (vía HACS)

1. En HACS → menú (⋮) → **Repositorios personalizados**
2. Añade la URL de este repositorio, categoría **Integración**
3. Instala "Blink (hardware_id fix)"
4. Reinicia Home Assistant
5. Si una integración Blink existente necesita autenticarse de nuevo, pulsa
   **Reautenticar** (o elimínala y añádela de nuevo desde cero)

Deberías ver ahora el paso del PIN de 2FA en vez del error inmediato de
"Invalid authentication", y las acciones de armar/desarmar deberían dejar
de fallar con `TokenRefreshFailed`.

## ⚠️ Notas importantes

- Esto **sustituye** la integración oficial `blink` mientras esté
  instalado vía `custom_components/blink` (Home Assistant prioriza
  `custom_components` sobre las integraciones nativas con el mismo
  dominio).
- Cuando Home Assistant publique finalmente un fix oficial, deberías
  **eliminar este repositorio personalizado de HACS** para volver a la
  integración oficial.
- No mantenido oficialmente por Home Assistant ni por Anthropic — es un
  pequeño parche manual, producido tras diagnosticar el problema con la
  ayuda de Claude (Anthropic).

## Contribuir / mantenerse al día

Este repo es una copia de `homeassistant/components/blink` de HA Core
2026.8.2, con los cambios de arriba. Si quieres rebasarlo tú mismo sobre
una versión más nueva de HA Core, compara `const.py` y `manifest.json`
con los ficheros oficiales de tu versión y reaplica los mismos cambios.

Issues y PRs bienvenidos.
