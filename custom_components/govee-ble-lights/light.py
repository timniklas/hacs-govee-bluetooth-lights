"""Platform for light integration."""
from __future__ import annotations
from typing import Any

import logging
_LOGGER = logging.getLogger(__name__)

import pygatt
from homeassistant.components.light import LightEntity

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    light = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([GoveeBluetoothLight(light)])

class GoveeBluetoothLight(LightEntity):
    """Representation of an Awesome Light."""

    def __init__(self, light) -> None:
        """Initialize an bluetooth light."""
        self._name = "GOVEE Light"
        self._state = None
        self._mac = light.address
        """self._led = BluetoothLED(light.address)"""
        adapter = pygatt.BGAPIBackend()
        adapter.start()
        device = adapter.connect(light.address)

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return self._mac.replace(":", "")

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs) -> None:
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._state = True

    def turn_off(self, **kwargs) -> None:
        """Instruct the light to turn off."""
        self._state = False

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """