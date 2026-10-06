# Ortsnetz Map Backend

**Version 1.0.1**

Home-Assistant-Custom-Integration für die **Ortsnetz Map Card**. Das Backend lädt die öffentlichen Karten-Messpunkte von `ortsnetz-auslastung.de` serverseitig, cached sie bedarfsgesteuert über einen `DataUpdateCoordinator` und stellt sie der Dashboard-Card über eine authentifizierte Home-Assistant-WebSocket-API bereit.

Dadurch ruft der Browser die externe Daten-API nicht direkt auf und CORS ist kein Problem.

## Funktionen

- Server-seitiger Abruf von `https://www.ortsnetz-auslastung.de/v1/map/points`
- Bedarfsgesteuerter Abruf: Daten werden nur geladen, wenn eine Card sie anfordert – kein Abruf beim Start und kein Hintergrund-Polling
- Cache von standardmäßig 5 Minuten; mehrere Cards und Browser teilen sich einen Abruf
- Nach einem fehlgeschlagenen Abruf standardmäßig 60 Sekunden Pause, solange werden die zuletzt geladenen Daten weiter ausgeliefert
- Home-Assistant `DataUpdateCoordinator`
- Cache-Dauer und Pause nach Fehlern nachträglich einstellbar (**Konfigurieren**)
- Authentifizierter WebSocket-Endpunkt `ortsnetz_map/get_points`
- Einrichtung vollständig über **Einstellungen → Geräte & Dienste**
- Keine Lovelace-Ressource im Backend-Repository – die Card wird separat über HACS installiert

## Installation über HACS

Automatisch

[![Open your Home Assistant instance and open this repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=BeGiBue&repository=home-assistant-ortsnetz-map&category=integration)

Manuell

1. In HACS **Benutzerdefinierte Repositories** öffnen.
2. Repository-URL hinzufügen und als Typ **Integration** auswählen.
3. **Ortsnetz Map Backend** installieren.
4. Home Assistant neu starten.
5. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Ortsnetz Map** öffnen und einrichten.
6. Zusätzlich die separate [Ortsnetz Map Card](https://github.com/BeGiBue/ortsnetz-map-card) über HACS installieren.

## Einstellungen

Unter **Einstellungen → Geräte & Dienste → Ortsnetz Map → Konfigurieren** lassen sich nach der Einrichtung ändern:

| Einstellung | Bereich | Standard | Wirkung |
|---|---|---|---|
| Cache-Dauer | 60–3600 s | 300 s | So lange werden Messpunkte ohne neuen Abruf ausgeliefert |
| Pause nach Fehler | 30–600 s | 60 s | So lange wird nach einem fehlgeschlagenen Abruf kein neuer Versuch gestartet |

Nach dem Speichern lädt die Integration automatisch neu.

## Datenfluss

```text
ortsnetz-auslastung.de
        ↓
Home Assistant Backend
  DataUpdateCoordinator
        ↓
authentifizierte HA WebSocket API
        ↓
Ortsnetz Map Card
```

## WebSocket API

Die Card verwendet:

```text
ortsnetz_map/get_points
```

Optional unterstützt der Endpunkt intern ein `refresh`-Flag, um vor der Antwort eine Aktualisierung anzufordern. Ein erneuter Abruf erfolgt dabei nur, wenn die gecachten Daten mindestens 60 Sekunden alt sind; andernfalls wird der Cache geliefert.

## Voraussetzungen

- Home Assistant 2026.6.0 oder neuer
- Internetzugriff des Home-Assistant-Servers auf `www.ortsnetz-auslastung.de`

## Hinweise

Dieses Projekt ist ein unabhängiges Community-Projekt und nicht Teil von `ortsnetz-auslastung.de` oder Home Assistant.

## Lizenz

GNU Affero General Public License v3.0 only (**AGPL-3.0-only**). Nutzung, Änderungen und Weitergabe sind unter den Bedingungen der AGPL erlaubt; abgeleitete Werke müssen unter derselben Lizenz stehen. Bei modifizierten Versionen, die über ein Netzwerk genutzt werden, muss der entsprechende Quellcode den Nutzern zugänglich gemacht werden. Details stehen in `LICENSE`.
