"""Constants for Ortsnetz Map."""

DOMAIN = "ortsnetz_map"
API_URL = "https://www.ortsnetz-auslastung.de/v1/map/points"

# Daten werden nur noch bei Bedarf (Card-Anfrage) geladen. Ein Cache-Eintrag
# gilt so lange als frisch; in dieser Zeit wird die externe API nicht erneut
# angefragt, egal wie viele Cards/Clients gleichzeitig offen sind.
CACHE_MAX_AGE_SECONDS = 300

# Untergrenze für ein explizit angefordertes Refresh ("refresh": true).
FORCED_REFRESH_MIN_AGE_SECONDS = 60

# Nach einem fehlgeschlagenen Abruf wird frühestens nach dieser Zeit erneut
# versucht, damit ein Ausfall der API nicht bei jeder Anfrage durchschlägt.
RETRY_AFTER_ERROR_SECONDS = 60

REQUEST_TIMEOUT_SECONDS = 30
