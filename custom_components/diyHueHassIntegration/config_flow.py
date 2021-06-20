import logging
from homeassistant import config_entries, exceptions
from . import DOMAIN
import os
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._discovered_devices = {}
        self._discovered_ip = None

    async def _async_try_connect(self, host):
        response = os.system("ping -c 1 " + host)
        if response == 0:
            return True
        else:
            return False

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                host = user_input["ipaddress"]
                valid = self._async_try_connect(host)
            except CannotConnect:
                errors["base"] = "cannot_connect"
                _LOGGER.error("Unable to connect to " + user_input["ipaddress"])
                return self.async_abort(reason="cannot_connect")

        if valid:
            await self.async_set_unique_id(user_input["serialnumber"])
            self._abort_if_unique_id_configured()
            _LOGGER.debug(
                "Success! Creating entry: "
                + user_input["name"]
                + " @ "
                + user_input["ipaddress"]
            )
            return self.async_create_entry(
                title=user_input["name"] + "@" + user_input["serialnumber"],
                data={
                    "Serialnumber": user_input["serialnumber"],
                    "Name": user_input["name"],
                    "IP": user_input["ipaddress"],
                    "Number_of_lights": user_input["number_of_lights"],
                },
            )

        data_schema = {
            vol.Required("serialnumber"): str,
            vol.Required("name"): str,
            vol.Required("ipaddress"): str,
            vol.Optional("number_of_lights", description={"suggested_value": 1}): int,
        }
        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(data_schema), errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Exception"""
