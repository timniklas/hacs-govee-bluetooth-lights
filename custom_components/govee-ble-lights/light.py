"""Platform for light integration."""

import logging
_LOGGER = logging.getLogger(__name__)

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (LightEntity)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Awesome Light platform."""
    # Add devices
    light = hass.data[DOMAIN][config.entry_id]
    new_devices = []
    new_devices.append(GoveeBluetoothLight(light))
    add_entities(new_devices)

class GoveeBluetoothLight(LightEntity):
    """Representation of an Awesome Light."""

    def __init__(self, light) -> None:
        """Initialize an bluetooth light."""
        self._name = "Light Name"
        self._state = True
        self._address = light.address

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return True

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

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