"""Platform for light integration."""
from __future__ import annotations
from typing import Any

import logging
_LOGGER = logging.getLogger(__name__)

from bleak import BleakClient
from homeassistant.components import bluetooth
from homeassistant.components.light import LightEntity

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    light = hass.data[DOMAIN][config_entry.entry_id]
    #bluetooth setup
    ble_device = await bluetooth.async_ble_device_from_address(hass, light.address.upper(), True)
    async with BleakClient(ble_device) as client:
        model_number = await ble_device.read_gatt_char("00002a24-0000-1000-8000-00805f9b34fb")
        _LOGGER.error("Model Number: {0}".format("".join(map(chr, model_number))))

    async_add_entities([GoveeBluetoothLight(light)])

class GoveeBluetoothLight(LightEntity):
    """Representation of an Awesome Light."""

    def __init__(self, light) -> None:
        """Initialize an bluetooth light."""
        self._name = "GOVEE Light"
        self._state = None
        self._mac = light.address

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