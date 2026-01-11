"""config file containing variable data."""

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.

    This class defines and validates all runtime configuration for the
    OpenWeather data fetcher. Values are read from OS environment variables
    or a local `.env` file (for development), validated on startup, and
    exposed as typed Python attributes.

    Required environment variables:
    - OPENWEATHER_API_KEY

    Optional environment variables:
    - OPENWEATHER_BASE_URL (default provided)
    - OPENWEATHER_TIMEOUT_S (default: 10.0)
    """

    openweather_api_key: str = Field(
        min_length=1,
        description="API key for the OpenWeather API",
    )
    openweather_timeout_s: float = Field(default=10.0, gt=0)
    openweather_base_url: HttpUrl = Field(
        default="https://api.openweathermap.org/data/3.0/onecall/timemachine",
        description="OpenWeather Time Machine endpoint",
    )

    model_config = SettingsConfigDict(
        env_file=".env",  # optional, used for local dev
        extra="ignore",  # ignore unrelated env vars
    )
