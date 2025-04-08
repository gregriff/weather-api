from api.config import CONFIG

NWS_BASE_URL = "https://api.weather.gov"
POINTS_URL = "/points/%{latitude:s},%{longitude:s}"
FORECAST_URL = "/gridpoints/%{office:s}/%{grid_x:d},%{grid_y:d}/forecast"
HOURLY_FORECAST_URL = "/gridpoints/%{office:s}/%{grid_x:d},%{grid_y:d}/forecast/hourly"
NWS_AUTH_HEADERS = {
    "User-Agent": f"{CONFIG.nws.user_agent_identifier}, {CONFIG.nws.user_agent_email}"
}
TEST_COORDS = (CONFIG.nws.test_lat, CONFIG.nws.test_long)
