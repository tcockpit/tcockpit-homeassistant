# Kurztexte Home Assistant (Website + App)

## Website (tcockpit.de, Abschnitt „Home Assistant“)
**TCockpit in Home Assistant.** Akkustand, Reichweite, Laden, Standort, Klima und Schloss deines Tesla direkt in Home Assistant.
1. In der App unter Mehr › Home Assistant einen Schlüssel erstellen und kopieren.
2. In HACS unter „Benutzerdefinierte Repositories“ `https://github.com/tcockpit/tcockpit-homeassistant` als Integration hinzufügen, „TCockpit“ installieren, Home Assistant neu starten.
3. Einstellungen → Geräte & Dienste → Integration hinzufügen → TCockpit, Schlüssel einfügen.
Lesen weckt das Auto nie. Steuern nur, wenn du es beim Schlüssel erlaubst.

## App (Mehr › Home Assistant, „So geht’s“) – so eingebaut ab Build 104
1. In TCockpit unter Mehr › Home Assistant einen API-Schlüssel erstellen und kopieren.
2. In Home Assistant HACS öffnen → oben rechts ⋮ → „Benutzerdefinierte Repositories“.
3. Repository https://github.com/tcockpit/tcockpit-homeassistant eintragen, Typ „Integration“, hinzufügen.
4. „TCockpit“ in HACS installieren und Home Assistant neu starten.
5. Einstellungen → Geräte & Dienste → Integration hinzufügen → „TCockpit“.
6. Den API-Schlüssel aus Mehr › Home Assistant einfügen. Fertig: Akku, Reichweite, Laden, Standort, Klima und Schloss erscheinen pro Fahrzeug.
