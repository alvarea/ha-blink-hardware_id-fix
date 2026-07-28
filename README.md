# Blink integration — hardware_id fix (unofficial)

Parche mínimo sobre la integración oficial `blink` de Home Assistant Core
(basado en la versión **2026.7.4**), que corrige el fallo de autenticación
("Invalid authentication" / login OAuth rechazado con `406 Not Acceptable`)
causado por que el servidor de Blink ahora exige que `hardware_id` tenga
formato UUID, mientras que Home Assistant sigue enviando el string literal
`"Home Assistant"`.

## Qué cambia

Un único cambio real, en `custom_components/blink/const.py`:

```diff
- HARDWARE_ID = "Home Assistant"
+ HARDWARE_ID = "a1b2c3d4-e5f6-47a8-9b12-abcdef123456"
```

Todo lo demás es idéntico al código oficial de HA 2026.7.4. También se
añadió el campo `"version"` en `manifest.json`, requerido por HACS para
integraciones personalizadas.

## Referencias del bug

- https://github.com/home-assistant/core/issues/158760
- https://github.com/home-assistant/core/issues/173520
- https://github.com/home-assistant/core/issues/176708
- https://community.home-assistant.io/t/blink-integration-broken-after-ha-restart-cannot-complete-2fa-pin-entry-eu-uk-sms-2fa/1013424/17

## Instalación

1. En HACS → menú (⋮) → **Repositorios personalizados**
2. Añade la URL de este repositorio, categoría **Integración**
3. Instala "Blink (hardware_id fix)"
4. Reinicia Home Assistant
5. Ve a la integración Blink existente y pulsa **Reautenticar** (o elimínala
   y añádela de nuevo desde cero)

## ⚠️ Importante

- Esto **reemplaza** la integración oficial `blink` mientras esté instalado
  vía `custom_components/blink` (HA prioriza `custom_components` sobre el
  código nativo).
- Al actualizar HA Core en el futuro, si Anthropic/HA publica un fix
  oficial, hay que **desinstalar este repositorio de HACS** para volver a
  usar la integración oficial (o quedará "congelada" en esta versión).
- No mantenido oficialmente por Home Assistant ni por Anthropic — es un
  parche manual de una sola línea, generado tras diagnosticar el fallo con
  ayuda de Claude.
