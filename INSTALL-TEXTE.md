# Kurztexte Home Assistant (Website + App)

## Website (tcockpit.de, Abschnitt „Home Assistant“)
**TCockpit in Home Assistant.** Akkustand, Reichweite, Laden, Standort, Klima und Schloss deines Tesla direkt in Home Assistant.
1. In der App unter Mehr → Einstellungen → Home Assistant einen Schlüssel erstellen und kopieren.
2. In HACS unter „Benutzerdefinierte Repositories“ `https://github.com/tcockpit/tcockpit-homeassistant` als Integration hinzufügen, „TCockpit“ installieren, Home Assistant neu starten.
3. Einstellungen → Geräte & Dienste → Integration hinzufügen → TCockpit, Schlüssel einfügen.
Lesen weckt das Auto nie. Steuern nur, wenn du es beim Schlüssel erlaubst.

## App (Mehr → Einstellungen → Home Assistant, „So geht’s“) – so eingebaut in Build 103
1. In Home Assistant HACS öffnen → oben rechts ⋮ → „Benutzerdefinierte Repositories“.
2. Repository https://github.com/tcockpit/tcockpit-homeassistant eintragen, Typ „Integration“, hinzufügen.
3. „TCockpit“ in HACS installieren und Home Assistant neu starten.
4. Einstellungen → Geräte & Dienste → Integration hinzufügen → „TCockpit“.
5. Den API-Schlüssel von hier einfügen. Fertig: Akku, Reichweite, Laden, Standort, Klima und Schloss erscheinen pro Fahrzeug.
