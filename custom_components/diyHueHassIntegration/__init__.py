import requests
from homeassistant.components import light
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_LIGHTS, CONF_NAME


DOMAIN = "diyHueHassIntegration"

CONF_NAME = "name"


async def async_setup(hass: HomeAssistant, config_entry):

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):

    device = diyHueEntity(entry)

    return True


class diyHueEntity:
    def __init__(self, entry: ConfigEntry):

        self._state = None
        self.lights = entry.data.get("number_of_lights")
        self.IP = entry.data.get("ipaddress")
        self.addr = "http://" + str(self.IP) + "/state"

    def turn_on(self):
        requests.post(
            url=self.addr, params={"on": True, "bri": 255, "xy": [0.53, 0, 21]}
        )

    def turn_off(self):
        requests.post(
            url=self.addr, params={"on": False, "bri": 0, "xy": [0.53, 0, 21]}
        )
