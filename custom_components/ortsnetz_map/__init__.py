"""Ortsnetz Map backend integration."""

from __future__ import annotations

import asyncio
import logging
from time import monotonic
from typing import Any

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_URL,
    CACHE_MAX_AGE_SECONDS,
    CONF_CACHE_MAX_AGE,
    CONF_RETRY_AFTER_ERROR,
    DOMAIN,
    FORCED_REFRESH_MIN_AGE_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
    RETRY_AFTER_ERROR_SECONDS,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

type OrtsnetzMapConfigEntry = ConfigEntry


class OrtsnetzDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch map points from ortsnetz-auslastung.de on demand and cache them.

    Es gibt kein festes Polling-Intervall (update_interval=None). Abgerufen wird
    nur, wenn ein Client Daten anfragt und der Cache veraltet ist.
    """

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name="Ortsnetz Map data",
            config_entry=entry,
            update_interval=None,
        )
        self._cache_max_age: int = entry.options.get(CONF_CACHE_MAX_AGE, CACHE_MAX_AGE_SECONDS)
        self._retry_after_error: int = entry.options.get(
            CONF_RETRY_AFTER_ERROR, RETRY_AFTER_ERROR_SECONDS
        )
        self._lock = asyncio.Lock()
        self._last_success: float | None = None
        self._last_attempt: float | None = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch current map data."""
        session = async_get_clientsession(self.hass)
        try:
            async with asyncio.timeout(REQUEST_TIMEOUT_SECONDS):
                response = await session.get(API_URL, headers={"Accept": "application/json"})
                response.raise_for_status()
                data = await response.json(content_type=None)
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Could not fetch Ortsnetz map data: {err}") from err

        if not isinstance(data, dict) or not isinstance(data.get("points"), list):
            raise UpdateFailed("Unexpected response from Ortsnetz map API")
        return data

    async def async_get_data(self, force: bool = False) -> dict[str, Any] | None:
        """Return cached data and refresh it first if needed.

        - Frischer Cache: keine Anfrage an die externe API.
        - Veralteter/leerer Cache: genau ein Abruf, parallele Anfragen warten
          auf dasselbe Ergebnis.
        - Schlägt der Abruf fehl, werden vorhandene Daten weiter ausgeliefert.
        """
        async with self._lock:
            now = monotonic()
            max_age = FORCED_REFRESH_MIN_AGE_SECONDS if force else self._cache_max_age
            cache_fresh = (
                self.data is not None
                and self._last_success is not None
                and now - self._last_success < max_age
            )
            in_error_cooldown = (
                not self.last_update_success
                and self._last_attempt is not None
                and now - self._last_attempt < self._retry_after_error
            )
            if not cache_fresh and not in_error_cooldown:
                self._last_attempt = monotonic()
                await self.async_refresh()
                if self.last_update_success:
                    self._last_success = monotonic()
            return self.data


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Register the authenticated WebSocket API."""
    websocket_api.async_register_command(hass, ws_get_points)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: OrtsnetzMapConfigEntry) -> bool:
    """Set up Ortsnetz Map from a config entry."""
    # Bewusst kein Abruf beim Start: Daten werden erst bei der ersten Card-Anfrage geladen.
    coordinator = OrtsnetzDataCoordinator(hass, entry)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    return True


async def async_unload_entry(hass: HomeAssistant, entry: OrtsnetzMapConfigEntry) -> bool:
    """Unload a config entry."""
    domain_data = hass.data.get(DOMAIN, {})
    domain_data.pop(entry.entry_id, None)
    if not domain_data:
        hass.data.pop(DOMAIN, None)
    return True


@websocket_api.websocket_command(
    {
        vol.Required("type"): "ortsnetz_map/get_points",
        vol.Optional("refresh", default=False): bool,
    }
)
@websocket_api.async_response
async def ws_get_points(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return cached Ortsnetz map data to an authenticated frontend client."""
    coordinators = hass.data.get(DOMAIN, {})
    if not coordinators:
        connection.send_error(msg["id"], "not_loaded", "Ortsnetz Map backend is not configured")
        return

    coordinator: OrtsnetzDataCoordinator = next(iter(coordinators.values()))
    data = await coordinator.async_get_data(force=msg["refresh"])

    if data is None:
        connection.send_error(msg["id"], "no_data", "No Ortsnetz data available")
        return

    connection.send_result(msg["id"], data)
