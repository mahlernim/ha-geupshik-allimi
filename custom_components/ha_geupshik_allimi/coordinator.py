from datetime import timedelta, datetime
import logging
import async_timeout

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_ATPT_OFCDC_SC_CODE, CONF_SD_SCHUL_CODE, CONF_API_KEY
from .api import GeupshikAPI

_LOGGER = logging.getLogger(__name__)

class GeupshikCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Geupshik data."""

    def __init__(self, hass: HomeAssistant, entry):
        """Initialize."""
        self.entry = entry
        self.api = GeupshikAPI(
            entry.data[CONF_ATPT_OFCDC_SC_CODE],
            entry.data[CONF_SD_SCHUL_CODE],
            entry.data.get(CONF_API_KEY)
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=3),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            # Note: explicit timeout control
            async with async_timeout.timeout(10):
                today = datetime.now()
                tomorrow = today + timedelta(days=1)
                
                # Fetch both days
                # If either fails, we raise an error to trigger retry? 
                # Or we return partial? Smart retry usually implies retrying the fetch.
                # So if connection fails, we fail.
                
                data_today = await self.api.get_lunch_data(today.strftime("%Y%m%d"))
                data_tomorrow = await self.api.get_lunch_data(tomorrow.strftime("%Y%m%d"))
                
                return {
                    "today": {
                        "date": today.strftime("%Y%m%d"),
                        "data": data_today
                    },
                    "tomorrow": {
                        "date": tomorrow.strftime("%Y%m%d"),
                        "data": data_tomorrow
                    }
                }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
