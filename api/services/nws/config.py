from api.config import CONFIG

BASE_URL = CONFIG.nws.root_url
POINTS_URL = "/points/%.4f,%.4f"
FORECAST_URL = "/gridpoints/%s/%d,%d/forecast"
HOURLY_FORECAST_URL = "/gridpoints/%s/%d,%d/forecast/hourly"
AUTH_HEADERS = {
    "User-Agent": f"{CONFIG.nws.user_agent_identifier}, {CONFIG.nws.user_agent_email}"
}
TEST_COORDS = (CONFIG.nws.test_lat, CONFIG.nws.test_long)
