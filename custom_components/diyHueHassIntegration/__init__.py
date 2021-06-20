from homeassistant.components import light
from . import diyHueLight
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_LIGHTS, CONF_NAME


DOMAIN = "diyHueHassIntegration"

CONF_NAME = "name"


async def async_setup(hass: HomeAssistant, config):
    conf = config.get(DOMAIN, {})

    return True


async def async_setup_entry(hass, config_entry, asnyc_add_devices):

    device = hass.data[DOMAIN][config_entry.entry_id]
    asnyc_add_devices(diyHueLight(device, config_entry, light))

    return True
