# Ortsnetz Map Backend 1.1.0-beta.2 (Vorabversion)

Zweite Testversion. Installation in HACS über **⋮ → Beta-Versionen anzeigen**. Ersetzt 1.1.0-beta.1, deren Tag noch auf einen Stand ohne Versionsangabe zeigte.

Neu gegenüber 1.1.0-beta.1:

- Cache-Dauer (60–3600 s, Standard 300 s) und Pause nach Fehlern (30–600 s, Standard 60 s) lassen sich unter **Einstellungen → Geräte & Dienste → Ortsnetz Map → Konfigurieren** ändern; die Integration lädt danach automatisch neu.
- Home Assistant zeigt jetzt die richtige Version an.

Weiterhin enthalten seit 1.1.0-beta.1:

- Daten werden nur noch abgerufen, wenn eine Card sie anfordert: kein Abruf beim Start und kein dauerhaftes Polling mehr.
- Parallele Anfragen mehrerer Cards oder Browser lösen höchstens einen Abruf aus.
- Das `refresh`-Flag des WebSocket-Befehls ruft nur neu ab, wenn der Cache mindestens 60 Sekunden alt ist.
- Nach einem fehlgeschlagenen Abruf werden vorhandene Daten weiter ausgeliefert.
- WebSocket-Befehl `ortsnetz_map/get_points` und Antwortformat unverändert.

Empfohlen zusammen mit Ortsnetz Map Card 1.0.3-beta.1.
