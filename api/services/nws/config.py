from api.config import CONFIG

_gridpoint_url_params = "{office:s}/{grid_x:d},{grid_y:d}"

NWS_BASE_URL = "https://api.weather.gov"
POINTS_URL = "/points/{latitude:s},{longitude:s}"
FORECAST_URL = f"/gridpoints/{_gridpoint_url_params}/forecast"
HOURLY_FORECAST_URL = f"/gridpoints/{_gridpoint_url_params}/forecast/hourly"
NWS_AUTH_HEADERS = {
    "User-Agent": f"{CONFIG.nws.user_agent_identifier}, {CONFIG.nws.user_agent_email}"
}
TEST_COORDS = (CONFIG.nws.test_lat, CONFIG.nws.test_long)
