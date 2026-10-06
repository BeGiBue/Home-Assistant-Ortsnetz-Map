# Ortsnetz Map Backend 1.1.0-beta.1 (Vorabversion)

Testversion für den bedarfsgesteuerten Datenabruf. Installation in HACS über **⋮ → Beta-Versionen anzeigen**.

- Daten werden nur noch abgerufen, wenn eine Card sie anfordert: kein Abruf beim Start und kein dauerhaftes Polling mehr.
- Cache von 5 Minuten; parallele Anfragen mehrerer Cards oder Browser lösen höchstens einen Abruf aus.
- Das `refresh`-Flag des WebSocket-Befehls ruft nur neu ab, wenn der Cache mindestens 60 Sekunden alt ist.
- Nach einem fehlgeschlagenen Abruf 60 Sekunden Pause; vorhandene Daten werden weiter ausgeliefert.
- WebSocket-Befehl `ortsnetz_map/get_points` und Antwortformat unverändert.

Empfohlen zusammen mit Ortsnetz Map Card 1.0.3-beta.1.
