# TCockpit für Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)

Bringt deinen Tesla aus der App **TCockpit** in Home Assistant: Akkustand, Reichweite, Laden, Standort, Klima und Schloss – pro Fahrzeug ein Gerät.

**Deutsch** · [English below](#english)

## Was du bekommst
- **Sensoren:** Akkustand, Reichweite, Ladestatus, Ladeleistung, Ladelimit, geladene Energie, Zeit bis voll, Innen-/Außentemperatur, Kilometerstand, Reifendruck, Software, Adresse
- **Binär-Sensoren:** lädt, Ladeklappe, Tür/Fenster/Kofferraum/Frunk offen, Wächtermodus, Klima an
- **Standort:** `device_tracker` pro Fahrzeug
- **Steuern (nur wenn dein Schlüssel es erlaubt):** Schalter Klima, Schalter Laden, Türschloss (Entriegeln nur mit extra Freigabe)

Lesen weckt das Auto nie. Abgefragt wird alle 60 Sekunden der letzte Stand vom TCockpit-Server.
Befehle laufen wie Befehle aus der App über den TCockpit-Server (Aufwecken, Wiederholen, Bestätigung als Mitteilung auf dem iPhone). Die Integration sendet nie von selbst einen Befehl.

## Installation
1. In der TCockpit-App: **Mehr → Einstellungen → Home Assistant → Schlüssel erstellen**. Für Schalter und Schloss „Steuern erlauben“ einschalten. Den Schlüssel kopieren (er wird nur einmal angezeigt).
2. In Home Assistant **HACS** öffnen → oben rechts **⋮ → Benutzerdefinierte Repositories**.
3. `https://github.com/tcockpit/tcockpit-homeassistant` eintragen, Typ **Integration**, hinzufügen.
4. **TCockpit** in HACS installieren und Home Assistant neu starten.
5. **Einstellungen → Geräte & Dienste → Integration hinzufügen → TCockpit** und den Schlüssel einfügen.

Schlüssel widerrufen: in der App unter Home Assistant nach links wischen. Home Assistant fragt dann nach einem neuen Schlüssel.

## Sicherheit
- Der Server speichert nur einen Fingerabdruck des Schlüssels, nicht den Schlüssel selbst.
- Ohne „Steuern erlauben“ kann der Schlüssel nur lesen.
- Entriegeln braucht zusätzlich „Auch Entriegeln erlauben“.
- Höchstens ein Befehl pro Fahrzeug alle 10 Sekunden.

---

## English

Brings your Tesla from the **TCockpit** app into Home Assistant: battery, range, charging, location, climate and lock – one device per vehicle.

### Entities
- **Sensors:** battery level, range, charging state, charger power, charge limit, energy added, time to full, inside/outside temperature, odometer, tire pressure, software, address
- **Binary sensors:** charging, charge port, door/window/trunk/frunk open, sentry mode, climate on
- **Location:** one `device_tracker` per vehicle
- **Controls (only if your key allows it):** climate switch, charging switch, door lock (unlock only with an extra permission)

Reading never wakes the car; the last known state is polled every 60 seconds.
Commands go through the TCockpit server exactly like app commands (wake, retry, confirmation push to your iPhone). The integration never sends a command on its own.

### Installation
1. In the TCockpit app: **Mehr → Einstellungen → Home Assistant → Schlüssel erstellen**. Enable "Steuern erlauben" for switches and lock. Copy the key (shown only once).
2. In Home Assistant open **HACS** → top right **⋮ → Custom repositories**.
3. Add `https://github.com/tcockpit/tcockpit-homeassistant`, type **Integration**.
4. Install **TCockpit** in HACS and restart Home Assistant.
5. **Settings → Devices & services → Add integration → TCockpit**, paste the key.

Revoke a key by swiping left in the app; Home Assistant will then ask for a new key.

## API (für Entwickler / for developers)
`Authorization: Bearer tck_…`
- `GET /api/ha/v1/info`
- `GET /api/ha/v1/vehicles`
- `GET /api/ha/v1/vehicles/{vin}/state`
- `POST /api/ha/v1/vehicles/{vin}/commands/{climate_on|climate_off|charge_start|charge_stop|lock|unlock}` (Body `{}`)
- `GET /api/ha/v1/jobs/{jobId}`

Kontakt / contact: kontakt@tcockpit.de
