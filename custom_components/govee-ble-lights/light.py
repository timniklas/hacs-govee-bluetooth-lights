"""Platform for light integration."""

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (LightEntity)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up the Govee Light ."""
    light = hass.data[DOMAIN][config_entry.entry_id]
    new_devices = []
    new_devices.append(GoveeBluetoothLight(light))
    async_add_entities(new_devices)


class GoveeBluetoothLight(LightEntity):
    """Representation of an Awesome Light."""

    def __init__(self, light) -> None:
        """Initialize an bluetooth light."""
        self._name = "Light Name"
        self._state = None
        self._brightness = None
        self._address = light.address

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._address)}}

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

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