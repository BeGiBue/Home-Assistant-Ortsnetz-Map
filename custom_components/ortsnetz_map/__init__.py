"""Ortsnetz Map backend integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import async_timeout
import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, DOMAIN, UPDATE_INTERVAL_MINUTES

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

type OrtsnetzMapConfigEntry = ConfigEntry


class OrtsnetzDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch and cache map points from ortsnetz-auslastung.de."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name="Ortsnetz Map data",
            update_interval=timedelta(minutes=UPDATE_INTERVAL_MINUTES),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch current map data."""
        session = async_get_clientsession(self.hass)
        try:
            async with async_timeout.timeout(30):
                response = await session.get(API_URL, headers={"Accept": "application/json"})
                response.raise_for_status()
                data = await response.json(content_type=None)
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Could not fetch Ortsnetz map data: {err}") from err

        if not isinstance(data, dict) or not isinstance(data.get("points"), list):
            raise UpdateFailed("Unexpected response from Ortsnetz map API")
        return data


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Register the authenticated WebSocket API."""
    websocket_api.async_register_command(hass, ws_get_points)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: OrtsnetzMapConfigEntry) -> bool:
    """Set up Ortsnetz Map from a config entry."""
    coordinator = OrtsnetzDataCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
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
    if msg.get("refresh"):
        await coordinator.async_request_refresh()

    if coordinator.data is None:
        connection.send_error(msg["id"], "no_data", "No Ortsnetz data available")
        return

    connection.send_result(msg["id"], coordinator.data)
