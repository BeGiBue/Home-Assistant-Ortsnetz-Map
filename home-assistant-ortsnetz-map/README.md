# Ortsnetz Map Backend for Home Assistant

Backend-Integration für die **Ortsnetz Map Card**. Sie lädt die Messpunkte von `ortsnetz-auslastung.de` serverseitig und stellt sie über eine authentifizierte Home-Assistant-WebSocket-API bereit. Dadurch muss die Card die externe API nicht direkt aus dem Browser aufrufen und CORS ist kein Problem.

> Diese Integration enthält bewusst **keine Lovelace-/Dashboard-Ressource**. Die Card liegt im separaten HACS-Dashboard-Repository `ortsnetz-map-card`.

## Installation über HACS

1. Dieses Repository nach GitHub hochladen, empfohlen unter dem Namen `home-assistant-ortsnetz-map`.
2. Vor dem ersten Release in `custom_components/ortsnetz_map/manifest.json` `YOUR_GITHUB_USERNAME` durch deinen GitHub-Benutzernamen ersetzen.
3. HACS → Benutzerdefinierte Repositories → Repository-URL hinzufügen → Typ **Integration**.
4. `Ortsnetz Map Backend` installieren.
5. Home Assistant neu starten.
6. Einstellungen → Geräte & Dienste → Integration hinzufügen → **Ortsnetz Map Backend**.
7. Zusätzlich das separate Dashboard-Repository `ortsnetz-map-card` über HACS installieren.

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

Die API-Daten werden im Backend standardmäßig alle fünf Minuten aktualisiert.

## WebSocket API

Die Card verwendet:

```text
ortsnetz_map/get_points
```

## Lizenz

MIT
