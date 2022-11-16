"""Platform for light integration."""
from __future__ import annotations
from typing import Any

import logging
_LOGGER = logging.getLogger(__name__)

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (LightEntity)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    light = hass.data[DOMAIN][config_entry.entry_id]
    new_devices = []
    new_devices.append(GoveeBluetoothLight(light))
    async_add_entities(new_devices)

class GoveeBluetoothLight(LightEntity):
    """Representation of an Awesome Light."""

    def __init__(self, light) -> None:
        """Initialize an bluetooth light."""
        self._name = "Light Name"
        self._state = True
        self._address = light.address

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "name": self._name,
            "manufacturer": "GOVEE",
        }

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs) -> None:
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """

    def turn_off(self, **kwargs) -> None:
        """Instruct the light to turn off."""

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """