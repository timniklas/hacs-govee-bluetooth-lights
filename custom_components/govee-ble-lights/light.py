"""Platform for light integration."""
from __future__ import annotations
from typing import Any

import logging
_LOGGER = logging.getLogger(__name__)

from enum import IntEnum

from bleak import BleakClient
from homeassistant.components import bluetooth
from homeassistant.components.light import LightEntity

from .const import DOMAIN

UUID_CONTROL_CHARACTERISTIC = '00010203-0405-0607-0809-0a0b0c0d2b11'

class LedCommand(IntEnum):
    """ A control command packet's type. """
    POWER      = 0x01
    BRIGHTNESS = 0x04
    COLOR      = 0x05

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    light = hass.data[DOMAIN][config_entry.entry_id]
    #bluetooth setup
    ble_device = bluetooth.async_ble_device_from_address(hass, light.address.upper(), True)
    async with BleakClient(ble_device) as client:
        await sendBluetoothData(client, LedCommand.POWER, [0x1])

    async_add_entities([GoveeBluetoothLight(light)])

async def sendBluetoothData(client, cmd, payload):
    if not isinstance(cmd, int):
        raise ValueError('Invalid command')
    if not isinstance(payload, bytes) and not (isinstance(payload, list) and all(isinstance(x, int) for x in payload)):
        raise ValueError('Invalid payload')
    if len(payload) > 17:
        raise ValueError('Payload too long')

    cmd = cmd & 0xFF
    payload = bytes(payload)

    frame = bytes([0x33, cmd]) + bytes(payload)
    # pad frame data to 19 bytes (plus checksum)
    frame += bytes([0] * (19 - len(frame)))
    
    # The checksum is calculated by XORing all data bytes
    checksum = 0
    for b in frame:
        checksum ^= b
    
    frame += bytes([checksum & 0xFF])
    await client.write_gatt_char(UUID_CONTROL_CHARACTERISTIC, frame, False)

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