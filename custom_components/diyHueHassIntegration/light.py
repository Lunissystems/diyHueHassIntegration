import json
from homeassistant.components.yeelight import DATA_CONFIG_ENTRIES
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import DOMAIN, HomeAssistant
import logging
import voluptuous as vol
import requests

from homeassistant.components import light

import homeassistant.helpers.config_validation as cv

from homeassistant.components.light import LightEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    device = hass.data[DOMAIN][DATA_CONFIG_ENTRIES][config_entry.entry_id]
    _LOGGER.debug("Adding %s", device.name)

    lights = []
    lights.append(diyHueLight(device, config_entry, LightEntity))
    async_add_entities(lights, True)


class diyHueLight(LightEntity):
    def __init__(self, device, config_entry, light):

        self._light = light
        self._name = config_entry.name
        self._state = None
        self._brightness = None

        """diyHueVariables"""
        self.lights = config_entry.number_of_lights
        self.IP = config_entry.ipaddress
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
        requests.post(
            url=self.addr, params={"on": True, "bri": 255, "xy": [0.53, 0, 21]}
        )

    def turn_off(self, **kwargs):
        requests.post(
            url=self.addr, params={"on": False, "bri": 0, "xy": [0.53, 0, 21]}
        )

    def update(self):
        """Fetch new state data for this light. This is the only method that should fetch new data for Home Assistant."""
        status = requests.get(url=self.addr)
        result = status.json()
        json.loads(result)

        self._light.update()

        self._state = result["on"]
        self._brightness = result["bri"]
