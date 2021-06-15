"""Platform for light integration."""
import logging

import voluptuous as vol
import requests

import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, PLATFORM_SCHEMA, LightEntity
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_USERNAME, default="admin"): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config[CONF_HOST]
    username = config[CONF_USERNAME]
    password = config.get(CONF_PASSWORD)

    # Setup connection with devices/cloud

    # Verify that passed in configuration works
    return True
    # Add devices
    """add_entities(AwesomeLight(light) for light in hub.lights())"""


class AwesomeLight(LightEntity):
    def __init__(self, light):
        """Initialize an AwesomeLight."""
        self._light = light
        self._name = light.name
        self._state = None
        self._brightness = None
        """diyHueVariables"""
        self.lights = 3
        self.IP = light.name
        self.addr = "http://" + self.IP + "/state"

    @property
    def name(self):
        return self._name

    @property
    def brightness(self):
        return self._brightness

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        para = {"on": true, "bri": 255, "xy": [0.53, 0, 21]}
        requests.post(url=self.addr, params=para)
        self._light.turn_on()

    def turn_off(self, **kwargs):
        ara = {"on": false, "bri": 0, "xy": [0.53, 0, 21]}
        requests.post(url=self.addr, params=ara)
        self._light.turn_off()

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._light.update()
        self._state = self._light.is_on()
        self._brightness = self._light.brightness
