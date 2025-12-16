from datetime import datetime
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the Geupshik Allimi sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        GeupshikSensor(coordinator, "Today", "today"),
        GeupshikSensor(coordinator, "Tomorrow", "tomorrow")
    ], True)


class GeupshikSensor(CoordinatorEntity, SensorEntity):
    """Representation of a School Meal Sensor."""

    def __init__(self, coordinator, name_suffix, data_key):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._name_suffix = name_suffix
        self._data_key = data_key
        # Access api from coordinator
        self._api = coordinator.api
        
        self._attr_name = f"HA식알리미 급식 {name_suffix}"
        self._attr_unique_id = f"{self._api._schul_code}_lunch_{name_suffix.lower()}"

    @property
    def icon(self):
        return "mdi:food-drumstick"
        
    @property
    def native_value(self):
        """Return the state of the sensor."""
        # Check if we have data for our specific day
        day_data = self.coordinator.data.get(self._data_key)
        if day_data and day_data.get('data'):
            return "Available"
        return "No Meal"

    @property
    def extra_state_attributes(self):
        """Return details about the meal."""
        day_container = self.coordinator.data.get(self._data_key) # {date: ..., data: ...}
        
        date_str = day_container['date']
        data = day_container.get('data')

        if data:
            raw_menu = data.get('DDISH_NM')
            cleaned_menu = self._api.clean_menu(raw_menu)
            school_name = data.get('SCHUL_NM', 'School')
            tts_text = self._api.format_tts(date_str, school_name, cleaned_menu)
            calories = data.get('CAL_INFO')
            
            return {
                "menu_clean": cleaned_menu,
                "menu_tts": tts_text,
                "calories": calories,
                "date": date_str,
                "school_name": school_name,
                "raw": raw_menu
            }
        else:
            # Generate "No meal" TTS
            dt = datetime.strptime(date_str, "%Y%m%d")
            spoken_date = dt.strftime("%Y년 %m월 %d일")
            tts_text = f"{spoken_date}, 오늘은 급식이 없습니다."
            
            return {
                "menu_clean": "None",
                "menu_tts": tts_text,
                "calories": None,
                "date": date_str
            }
