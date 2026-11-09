# TCockpit für Home Assistant

Offizielle HACS-Integration für [TCockpit](https://tcockpit.de) — Sensoren und Steuerung für Tesla-Fahrzeuge, optional Energy Site und Wall Connector (nur Anzeige).

## Version 0.4.0

- Alles aus 0.3.0, plus Fleet-Telemetrie/Befehle:
  - Homelink-Button, Boombox/Furz-Button
  - Valet-Modus und Geschwindigkeitsbegrenzung per **Service mit PIN** (PIN wird nie gespeichert)
  - Sitzkühlung (Select), automatische Sitz-/Lenkradklima (Switch)
  - Batterieheizung, Fahrer anwesend, TPMS-Warnungen, Pack V/A, Modul-Temperaturen
  - Phantomverbrauch / Standverlust (30 Tage) aus der TCockpit-DB
  - Software-Update installieren via `schedule_software_update` (wenn Key Steuerung erlaubt)
  - Ladekabelschloss-**Status** (Latch) bereits in 0.3; kein eigener Lock-Befehl bei Tesla
- Energy Site + Wall Connector: **read-only** in HA; braucht Scope `energy_device_data` nach Re-Login in der App
- Öffnen nur mit **Entriegeln erlauben**; Lesen weckt nie

## Installation (HACS)

1. HACS → ⋮ → Benutzerdefinierte Repositories → `https://github.com/tcockpit/tcockpit-homeassistant` (Typ: Integration)
2. TCockpit installieren / auf **v0.4.0** aktualisieren → Home Assistant neu starten
3. Einstellungen → Geräte & Dienste → Integration hinzufügen → TCockpit
4. API-Schlüssel aus der App: **Mehr → Home Assistant**

## Energy / Wallbox

Scopes müssen in der Tesla-Developer-App freigeschaltet sein **und** Michael muss in der TCockpit-App **erneut bei Tesla anmelden**. Nur Portal-Freigabe reicht nicht — der gespeicherte Token bekommt die Scopes erst beim Re-Login. Ohne Scope bleiben Energy-Entitäten leer.

## Services (PIN)

- `tcockpit.valet_mode` — `vin`, `enabled`, `pin` (4–8 Ziffern)
- `tcockpit.speed_limit` — `vin`, `action` (`activate` / `deactivate` / `clear_pin`), `pin` (4 Ziffern)
- `tcockpit.send_command` — beliebiger Allowlist-Befehl inkl. Parameter

## Nicht möglich (ehrlich)

- **Dashcam** als eigener Sensor: kein Fleet-Telemetry-Feld (nur schwaches `CenterDisplay`)
- **Schlüsselloses Fahren** (Tessie): kein äquivalenter Fleet-Befehl / Telemetrie-Flag
- **Ladekabel verriegeln/entriegeln** als Befehl: Tesla bietet nur Latch-Status, keinen Lock-Command
- Energy-Steuerung (Storm Watch etc.): bewusst HA-Anzeige only

## Lizenz

MIT — siehe LICENSE.

---

# TCockpit for Home Assistant

Official HACS integration for [TCockpit](https://tcockpit.de) — sensors and controls for Tesla vehicles, optional Energy Site and Wall Connector (display only).

## Version 0.4.0

- Everything from 0.3.0, plus Fleet telemetry/commands:
  - Homelink button, boombox/fart button
  - Valet mode and speed limit via **PIN services** (PIN never stored)
  - Seat cooling (select), auto seat/steering climate (switches)
  - Battery heater, driver present, TPMS warnings, pack V/A, module temps
  - Phantom drain / idle loss (30d) from the TCockpit DB
  - Software update install via `schedule_software_update` when the key allows control
  - Charge cable latch **status** (from 0.3); Tesla has no lock command
- Energy Site + Wall Connector: **read-only** in HA; needs `energy_device_data` after app re-login
- Opening actions need **Allow unlock**; reading never wakes the car

## Install (HACS)

1. HACS → ⋮ → Custom repositories → `https://github.com/tcockpit/tcockpit-homeassistant` (Integration)
2. Install / update to **v0.4.0** → restart Home Assistant
3. Settings → Devices & services → Add → TCockpit
4. API key from the app: **More → Home Assistant**

## Energy / Wall Connector

Scopes must be enabled on the Tesla developer app **and** Michael must **re-login to Tesla in the TCockpit app**. Portal approval alone does not update the stored token. Without the scope, energy entities stay empty.

## PIN services

- `tcockpit.valet_mode` — `vin`, `enabled`, `pin`
- `tcockpit.speed_limit` — `vin`, `action` (`activate` / `deactivate` / `clear_pin`), `pin`
- `tcockpit.send_command` — any allowlisted command

## Not available

- Dedicated **dashcam** sensor (no Fleet Telemetry field)
- Tessie **keyless driving** equivalent
- Charge cable **lock/unlock command** (latch status only)
- Energy site controls (display only by design)

## License

MIT — see LICENSE.
