from api.config import CONFIG

POINTS_URL = f"{CONFIG.nws.root_url}/points"
GRIDPOINTS_URL = f"{CONFIG.nws.root_url}/gridpoints"
AUTH_HEADERS = {
    "User-Agent": f"{CONFIG.nws.user_agent_identifier}, {CONFIG.nws.user_agent_email}"
}
TEST_COORDS = (CONFIG.nws.test_lat, CONFIG.nws.test_long)
