# Weather API

[FastAPI](https://fastapi.tiangolo.com/) backend for a weather app. Uses the [National Weather Service API](https://www.weather.gov/documentation/services-web-api) and Mapbox's [Geocoding API](https://docs.mapbox.com/api/search/geocoding/#forward-geocoding-with-search-text-input). Uses [SQLAlchemy](https://www.sqlalchemy.org/) to define DDL and make queries and migrations RDBMS-agnostic.
Focus on maintainable and scalable design.

### Local Development

- ###### Set up Virtual Environment
- ###### Install Dependencies: `python -m pip install -r requirements.txt --require-hashes`
- ###### (For searchbox features): [Create Mapbox account](https://console.mapbox.com/) and API key
- ###### Create, populate env file: `cp example.env.json dev.env.json` (running dev server will tell you if anything is missing)
- ###### Run dev server: `python -m uvicorn api.main:app --reload --log-level debug`

### Roadmap

- Optional OIDC login system with Keycloak. DB is already set up for this
- Manual containerized deployment, hosted by Cloudflare Tunnels
