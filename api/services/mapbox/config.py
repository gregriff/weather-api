from api.config import CONFIG

MAPBOX_BASE_URL = "https://api.mapbox.com/search/geocode/v6"
MAPBOX_ACCESS_TOKEN = CONFIG.mapbox.public_token
FORWARD_GEOCODE_URL = "/forward?q={query}&country=us&proximity={longitude}%2C{latitude}&types=place&worldview=us&access_token={access_token}"
