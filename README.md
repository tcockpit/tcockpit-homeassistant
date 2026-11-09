# TCockpit für Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)

Bringt deinen Tesla aus der App **TCockpit** in Home Assistant: Status und alle Befehle, die die App kann – pro Fahrzeug ein Gerät.

**Deutsch** · [English below](#english)

## Was du bekommst
- **Sensoren:** Akkustand, Reichweite, Ladestatus, Ladeleistung, Ladelimit, geladene Energie, Zeit bis voll, Innen-/Außentemperatur, Kilometerstand, Reifendruck, Software, Adresse, Verbindung
- **Binär-Sensoren:** lädt, Ladeklappe, Tür/Fenster/Kofferraum/Frunk offen, Wächtermodus, Klima an
- **Standort:** `device_tracker` pro Fahrzeug
- **Steuern** (nur wenn dein Schlüssel „Steuern erlauben“ hat):
  - **Klima:** Klima-Entity (An/Aus + Zieltemperatur), Defrost/Max, Klimahaltemodus (Halten/Hund/Camp), Sitzheizungen, Lenkradheizung, Bioweapon, Überhitzungsschutz, Zubehörstrom, Energiesparmodus
  - **Laden:** Schalter Laden, Ladelimit (Number), Ladestrom (Number)
  - **Buttons:** Hupe, Lichthupe, Aufwecken, Media (Play/Pause, Titel, Lautstärke), Ladeklappe schließen, Fenster schließen
  - **Schloss:** verriegeln; entriegeln nur mit „Auch Entriegeln erlauben“
  - **Öffnen** (braucht „Auch Entriegeln erlauben“): Kofferraum, Frunk, Ladeklappe öffnen, Fenster lüften
  - **Service** `tcockpit.send_command` für jeden freigegebenen Befehl inkl. Lade-/Abfahrtsplan

Lesen weckt das Auto nie. Abgefragt wird alle 60 Sekunden der letzte Stand vom TCockpit-Server.
Befehle laufen wie Befehle aus der App über den TCockpit-Server (Aufwecken, Wiederholen, Bestätigung als Mitteilung auf dem iPhone). Die Integration sendet nie von selbst einen Befehl.

## Installation
1. In der TCockpit-App: **Mehr › Home Assistant → Schlüssel erstellen**. Für Schalter und Schloss „Steuern erlauben“ einschalten. Den Schlüssel kopieren (er wird nur einmal angezeigt).
2. In Home Assistant **HACS / Marktplatz** öffnen → oben rechts **⋮ → Benutzerdefinierte Repositories**.
3. `https://github.com/tcockpit/tcockpit-homeassistant` eintragen, Typ **Integration**, hinzufügen.
4. **TCockpit** installieren und Home Assistant neu starten (bzw. in HACS auf die neue Version aktualisieren).
5. **Einstellungen → Geräte & Dienste → Integration hinzufügen → TCockpit** und den Schlüssel einfügen.

Schlüssel widerrufen: in der App unter Home Assistant nach links wischen. Home Assistant fragt dann nach einem neuen Schlüssel.

## Sicherheit
- Der Server speichert nur einen Fingerabdruck des Schlüssels, nicht den Schlüssel selbst.
- Ohne „Steuern erlauben“ kann der Schlüssel nur lesen.
- Entriegeln und Öffnen (Kofferraum/Frunk/Ladeklappe/Fenster) brauchen zusätzlich „Auch Entriegeln erlauben“.
- Höchstens ein Befehl pro Fahrzeug alle 10 Sekunden.

---

## English

Brings your Tesla from the **TCockpit** app into Home Assistant: status and every command the app supports – one device per vehicle.

### Entities
- **Sensors:** battery, range, charging state/power/limit/energy/ETA, temps, odometer, tires, software, address, presence
- **Binary sensors:** charging, charge port, door/window/trunk/frunk open, sentry, climate on
- **Location:** one `device_tracker` per vehicle
- **Controls** (only if the key allows control):
  - **Climate** entity (on/off + target temp), defrost/max, climate keeper, seat heaters, steering wheel heater, bioweapon, cabin overheat protection, keep accessory power, low power mode
  - **Charging** switch, charge limit (number), charging amps (number)
  - **Buttons:** honk, flash, wake, media, close charge port, close windows
  - **Lock:** lock; unlock only with the unlock permission
  - **Opening** (needs unlock permission): trunk, frunk, open charge port, vent windows
  - **Service** `tcockpit.send_command` for any allowlisted command including schedules

Reading never wakes the car. Commands use the same durable queue as the app.

### Installation
1. In the TCockpit app: **Mehr › Home Assistant → create key**. Enable control for switches/lock. Copy the key (shown once).
2. In Home Assistant open **HACS / Marketplace** → **⋮ → Custom repositories**.
3. Add `https://github.com/tcockpit/tcockpit-homeassistant`, type **Integration**.
4. Install/update **TCockpit** and restart Home Assistant.
5. **Settings → Devices & services → Add integration → TCockpit**, paste the key.

## API (for developers)
`Authorization: Bearer tck_…`
- `GET /api/ha/v1/info` → `commands` lists what this key may call
- `GET /api/ha/v1/vehicles`
- `GET /api/ha/v1/vehicles/{vin}/state`
- `POST /api/ha/v1/vehicles/{vin}/commands/{name}` with JSON body (`idempotencyKey` optional; extra fields are command parameters, e.g. `{"celsius":21}`, `{"percent":80}`, `{"amps":16}`, `{"mode":"dog"}`, `{"seat":0,"level":2}`)
- `GET /api/ha/v1/jobs/{jobId}`

Kontakt / contact: kontakt@tcockpit.de
