import re
import aiohttp
import asyncio
from datetime import datetime

URL = "https://open.neis.go.kr/hub/mealServiceDietInfo"

class GeupshikAPI:
    """Helper class to fetch and clean school meal data."""

    def __init__(self, atpt_code, schul_code, api_key=None):
        self._atpt_code = atpt_code
        self._schul_code = schul_code
        self._api_key = api_key

    async def get_lunch_data(self, date_str):
        """Fetch lunch data for a specific date (YYYYMMDD)."""
        params = {
            "Type": "json",
            "ATPT_OFCDC_SC_CODE": self._atpt_code,
            "SD_SCHUL_CODE": self._schul_code,
            "MLSV_YMD": date_str
        }
        if self._api_key:
            params["KEY"] = self._api_key

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(URL, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()

                    # Check for errors or empty data
                    if "mealServiceDietInfo" not in data:
                        return None
                    
                    # Extract the row (lunch is typically index 0 if only lunch provided, but let's be safe)
                    # The API might return multiple rows if breakfast/dinner exists.
                    # Usually "MMEAL_SC_CODE" 2 is Lunch.
                    rows = data["mealServiceDietInfo"][1]["row"]
                    lunch_row = next((row for row in rows if row["MMEAL_SC_CODE"] == "2"), None)
                    
                    if not lunch_row:
                        # Fallback: if only one row, assume it's what we want or return the first
                        if rows:
                            return rows[0]
                        return None
                        
                    return lunch_row
            except Exception as e:
                # Log error or re-raise? For now, return None so sensor shows "Unavailable"
                return None

    def clean_menu(self, raw_menu):
        """Clean up the menu text for TTS."""
        if not raw_menu:
            return ""
            
        # 1. Remove all content in parentheses (allergy codes, kitchen notes like '2담기')
        cleaned = re.sub(r'\([^)]*\)', '', raw_menu)

        # 2. Remove fractions like 1/2, 1/3 (e.g. 바나나1/2 -> 바나나)
        cleaned = re.sub(r'\d+/\d+', '', cleaned)
        
        # 3. Replace <br/> and remaining slashes with commas
        cleaned = cleaned.replace('<br/>', ', ').replace('/', ', ')
        
        # 4. Remove special characters (stars, hearts, bullets etc.)
        cleaned = re.sub(r'[★♥♡●■□▲▼◆◇]', '', cleaned)
        
        # 5. Collapse multiple spaces/commas
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r',\s*,', ',', cleaned) # remove double commas
        cleaned = cleaned.strip(', ')
        
        return cleaned

    def format_tts(self, date_str, school_name, cleaned_menu):
        """Format the spoken text."""
        dt = datetime.strptime(date_str, "%Y%m%d")
        spoken_date = dt.strftime("%Y년 %m월 %d일")
        
        if not cleaned_menu:
            return f"{spoken_date}, 오늘은 급식이 없습니다."
            
        return f"{spoken_date}, {school_name} 오늘의 급식 메뉴를 알려드릴게요. {cleaned_menu} 입니다."
