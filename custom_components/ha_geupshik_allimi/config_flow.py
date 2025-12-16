import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_ATPT_OFCDC_SC_CODE, CONF_SD_SCHUL_CODE, CONF_API_KEY

class GeupshikAllimiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HA Geupshik Allimi."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate input if needed (checks could be added here)
            # For now, we trust the inputs and create the entry.
            return self.async_create_entry(title="School Meal Info", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_ATPT_OFCDC_SC_CODE): str,
            vol.Required(CONF_SD_SCHUL_CODE): str,
            vol.Optional(CONF_API_KEY): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
