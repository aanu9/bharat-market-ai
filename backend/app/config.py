import json
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "BHARAT MARKET AI"
    upstox_access_token: str = ""
    upstox_instrument_keys: str = "{}"
    gdelt_timespan: str = "24h"
    frontend_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def instruments(self):
        try:
            value = json.loads(self.upstox_instrument_keys or "{}")
            return value if isinstance(value, dict) else {}
        except json.JSONDecodeError:
            return {}

settings = Settings()
