# TCockpit für Home Assistant

Offizielle HACS-Integration für [TCockpit](https://tcockpit.de) — Sensoren und Steuerung für Tesla-Fahrzeuge, optional Energy Site und Wall Connector (nur Anzeige).

## Version 0.3.0

- Fahrzeug: Tessie-Parität für JP (Online-Status, Türen/Fenster einzeln, Covers für Kofferraum/Frunk/Ladeklappe/Fenster, Mediaplayer, Update-Anzeige, Navigation/Route, Lade-Details, Akkugesundheit aus Telemetrie)
- Energy Site + Wall Connector: **read-only**, nur in Home Assistant (nicht in der App). Braucht Tesla-Scope `energy_device_data` (nach Re-Login)
- Öffnen (Kofferraum, Frunk, Ladeklappe, Fenster lüften, Entriegeln) nur mit **Entriegeln erlauben**
- Lesen weckt das Auto nie; Befehle laufen über dieselbe Queue wie die App

## Installation (HACS)

1. HACS → ⋮ → Benutzerdefinierte Repositories → `https://github.com/tcockpit/tcockpit-homeassistant` (Typ: Integration)
2. TCockpit installieren / auf **v0.3.0** aktualisieren → Home Assistant neu starten
3. Einstellungen → Geräte & Dienste → Integration hinzufügen → TCockpit
4. API-Schlüssel aus der App: **Mehr → Home Assistant**

## Energy / Wallbox

Nach dem Update muss Michael in der TCockpit-App **erneut bei Tesla anmelden**, damit die Scopes `energy_device_data` und `energy_cmds` erteilt werden. Zusätzlich müssen diese Scopes in der Tesla-Developer-App freigeschaltet sein. Ohne Scope bleiben die Energy-Entitäten leer/`unavailable`.

## Nicht möglich (ehrlich)

Homelink, Furz, Schlüsselloses Fahren, Valet, Sitzkühlung, Dashcam, „Benutzer anwesend“, automatische Sitz-/Lenkradklima, Batterieheizung, Reifendruck-*Warnungen*, Pack-Strom/Spannung, Modul-Temperaturen, Software-*Installieren* (nur Versionsanzeige) — fehlen in unserer Fleet-Telemetrie bzw. Command-Allowlist.

## Lizenz

MIT — siehe LICENSE.

---

# TCockpit for Home Assistant

Official HACS integration for [TCockpit](https://tcockpit.de) — sensors and controls for Tesla vehicles, optional Energy Site and Wall Connector (display only).

## Version 0.3.0

- Vehicle: Tessie parity (online status, per-door/window, covers, media player, update entity, nav/route, charge details, battery health from telemetry)
- Energy Site + Wall Connector: **read-only**, HA only (not in the app). Needs Tesla scope `energy_device_data` after re-login
- Opening actions require **Allow unlock**; reading never wakes the car

## Install (HACS)

1. HACS → ⋮ → Custom repositories → `https://github.com/tcockpit/tcockpit-homeassistant` (Integration)
2. Install / update to **v0.3.0** → restart Home Assistant
3. Settings → Devices & services → Add → TCockpit
4. API key from the app: **More → Home Assistant**

## Energy / Wall Connector

Re-login to Tesla in the TCockpit app so `energy_device_data` (+ `energy_cmds`) are granted. Those scopes must also be enabled on the Tesla developer app. Without the scope, energy entities stay empty.

## Not available

Homelink, fart, keyless driving, valet, seat cooling, dashcam, user present, auto seat/steer climate, battery heater, tire pressure *warnings*, pack current/voltage, module temps, software *install* (version display only).

## License

MIT — see LICENSE.
