*[Read in English](README.md)*

# Blink integration — fix del hardware_id (no oficial)

Parche mínimo sobre la integración oficial `blink` de Home Assistant Core
(basado en la versión **2026.8.2**, blinkpy `0.25.9`) que corrige el fallo
de autenticación ("Invalid authentication" / login OAuth rechazado con
`406 Not Acceptable`) causado por que el servidor de Blink ahora exige
que `hardware_id` tenga formato UUID, mientras que Home Assistant sigue
enviando el string literal `"Home Assistant"`.

## ⚠️ Antes de instalar: genera TU PROPIO UUID

**No uses el UUID de ejemplo que trae `const.py` en este repo.** Cada
instalación necesita su propio `hardware_id`, único y privado. Reutilizar
el mismo valor en distintas cuentas/instalaciones de Blink puede hacer que
los sistemas antifraude de Blink bloqueen ese valor — que es exactamente
lo que le pasó al autor original tras compartir este fix en el foro de la
comunidad de Home Assistant con un UUID real y funcional metido en el
código. La autenticación volvió a fallar para todo el que usaba ese
mismo valor compartido.

**Genera el tuyo antes de instalar:**

```bash
# macOS / Linux
uuidgen

# Python (cualquier sistema)
python3 -c "import uuid; print(uuid.uuid4())"
```

Luego edita `custom_components/blink/const.py` y sustituye el
`HARDWARE_ID` de ejemplo por tu propio valor generado, **antes** de
añadir esto como repositorio personalizado en HACS / antes de la primera
descarga.

Si ya instalaste una versión anterior de este fix con el UUID
compartido, genera uno nuevo y privado, actualiza tu `const.py` local,
y sube el cambio a tu propia copia/fork de este repo antes de actualizar
vía HACS.

## Qué cambia

Un único cambio real, en `custom_components/blink/const.py`:

```diff
- HARDWARE_ID = "Home Assistant"
+ HARDWARE_ID = "<tu-propio-uuid-privado>"
```

Todo lo demás es idéntico al código oficial de HA 2026.8.2. También se
añadió el campo `"version"` en `manifest.json`, requerido por HACS para
integraciones personalizadas, y se fija `blinkpy` a la versión `0.25.9`
(la misma que trae HA 2026.8.x), que además resuelve un bug distinto de
`TokenRefreshFailed` al armar/desarmar y al actualizar imágenes de
cámaras (ver más abajo).

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

1. Genera tu propio UUID privado (ver arriba) y edita
   `custom_components/blink/const.py` en tu propia copia/fork de este repo
2. En HACS → menú (⋮) → **Repositorios personalizados**
3. Añade la URL de este repositorio, categoría **Integración**
4. Instala "Blink (hardware_id fix)"
5. Reinicia Home Assistant
6. Ve a tu integración Blink existente y pulsa **Reautenticar** (o
   elimínala y añádela de nuevo desde cero) — esto es esperado: cambiar
   el `hardware_id` invalida cualquier sesión anterior, así que tendrás
   que pasar el 2FA otra vez esta vez

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
con los ficheros oficiales de tu versión y reaplica los mismos cambios
(recordando usar tu propio UUID privado, no uno compartido).

Issues y PRs bienvenidos.
