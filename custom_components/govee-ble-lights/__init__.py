"""The Govee Bluetooth BLE integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import hub

from .const import DOMAIN

PLATFORMS: list[str] = ["light"]

class Hub:
    manufacturer = "Demonstration Corp"
    def __init__(self, hass: HomeAssistant, address: str) -> None:
        """Init dummy hub."""
        self._address = address


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Govee BLE device from a config entry."""
    address = entry.unique_id
    assert address is not None
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = Hub(hass, address=address)
    await hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok