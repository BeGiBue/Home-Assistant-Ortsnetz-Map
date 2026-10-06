# Changelog

## Unreleased

- Options-Flow: Cache-Dauer (60–3600 s) und Pause nach Fehlern (30–600 s) lassen sich unter **Konfigurieren** nachträglich ändern; die Integration lädt danach automatisch neu.

## 1.1.0-beta.1 (Vorabversion)

- Daten werden bedarfsgesteuert abgerufen: kein Abruf beim Start und kein dauerhaftes Polling mehr, sondern nur bei Anfrage einer Card.
- Cache von 5 Minuten; parallele Anfragen lösen höchstens einen Abruf aus.
- `refresh`-Flag des WebSocket-Befehls ruft nur neu ab, wenn der Cache mindestens 60 Sekunden alt ist.
- Nach einem fehlgeschlagenen Abruf 60 Sekunden Pause; vorhandene Daten werden weiter ausgeliefert.
- `async_timeout` durch `asyncio.timeout` ersetzt.
- Tests mit `pytest-homeassistant-custom-component` und GitHub-Workflow ergänzt.

## 1.0.1

- Lizenz auf GNU Affero General Public License v3.0 only (AGPL-3.0-only) umgestellt.
- HACS-Ländermetadaten für Deutschland ergänzt.
- Repository für die Aufnahme in die HACS-Standardliste vorbereitet.

## 1.0.0

- Erstes stabiles Release.
- Serverseitiger Abruf und Cache der Ortsnetz-Kartenpunkte.
- Authentifizierte Home-Assistant-WebSocket-API.
- Config Flow für die Einrichtung über die Benutzeroberfläche.
- Backend und Dashboard-Card als getrennte HACS-Repositories.
- Lizenz: CC BY-NC 4.0.
