# Ortsnetz Map Backend

**Version 1.0.0**

Home-Assistant-Custom-Integration für die **Ortsnetz Map Card**. Das Backend lädt die öffentlichen Karten-Messpunkte von `ortsnetz-auslastung.de` serverseitig, cached sie über einen `DataUpdateCoordinator` und stellt sie der Dashboard-Card über eine authentifizierte Home-Assistant-WebSocket-API bereit.

Dadurch ruft der Browser die externe Daten-API nicht direkt auf und CORS ist kein Problem.

## Funktionen

- Server-seitiger Abruf von `https://www.ortsnetz-auslastung.de/v1/map/points`
- Standard-Aktualisierung alle 5 Minuten
- Home-Assistant `DataUpdateCoordinator`
- Authentifizierter WebSocket-Endpunkt `ortsnetz_map/get_points`
- Einrichtung vollständig über **Einstellungen → Geräte & Dienste**
- Keine Lovelace-Ressource im Backend-Repository – die Card wird separat über HACS installiert

## Installation über HACS

1. Dieses Repository auf GitHub bereitstellen, empfohlen als `home-assistant-ortsnetz-map`.
2. In HACS **Benutzerdefinierte Repositories** öffnen.
3. Repository-URL hinzufügen und als Typ **Integration** auswählen.
4. **Ortsnetz Map Backend** installieren.
5. Home Assistant neu starten.
6. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Ortsnetz Map** öffnen und einrichten.
7. Zusätzlich das separate HACS-Dashboard-Repository `ortsnetz-map-card` installieren.

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

Optional unterstützt der Endpunkt intern ein `refresh`-Flag, um vor der Antwort eine Aktualisierung anzufordern.

## Voraussetzungen

- Home Assistant 2026.6.0 oder neuer
- Internetzugriff des Home-Assistant-Servers auf `www.ortsnetz-auslastung.de`

## Hinweise

Dieses Projekt ist ein unabhängiges Community-Projekt und nicht Teil von `ortsnetz-auslastung.de` oder Home Assistant.

## Lizenz

Creative Commons Attribution-NonCommercial 4.0 International (**CC BY-NC 4.0**). Änderungen und nicht-kommerzielle Weitergabe sind unter Namensnennung erlaubt; kommerzielle Nutzung ist nicht gestattet. Details stehen in `LICENSE`.
