# Declarative code that generates RDBMS-agnostic DDL
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import func
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.types import (
    CHAR,
    NUMERIC,
    UUID,
    VARCHAR,
    Boolean,
    DateTime,
    SmallInteger,
)


class Base(DeclarativeBase):
    pass


# Many-Many association tables
settings_cities_association = Table(
    "saved_cities",
    Base.metadata,
    Column("settings_id", ForeignKey("settings.user_id"), primary_key=True, index=True),
    Column("city_id", ForeignKey("cities.id"), primary_key=True, index=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(VARCHAR(length=20), unique=False)
    email: Mapped[str] = mapped_column(VARCHAR(length=50), unique=True)

    date_created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_modified: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.utc_timestamp()
    )

    # ORM-specific declarations. This allows us to use dot-access on Python instances of Rows to access their relationships for updates and deletes
    # this will auto-JOIN the `settings` table when we make a SELECT on `users`
    settings: Mapped["UserSettings"] = relationship(
        "Settings",
        back_populates="user",
    )


class UserSettings(Base):
    __tablename__ = "settings"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), primary_key=True, index=True
    )

    # there will be a use for this at some point
    favorite_city_id: Mapped[str] = mapped_column(
        ForeignKey("cities.id"), nullable=True
    )

    # used to fetch weather data for last-known location of user as soon as app loads
    last_known_gridpoint_x: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    last_known_gridpoint_y: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    # actual settings
    celcius: Mapped[bool] = mapped_column(Boolean, default=False)

    date_created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_modified: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.utc_timestamp()
    )

    # ORM-specific declarations and relationships
    user: Mapped["User"] = relationship(back_populates="settings")
    favorite_city: Mapped[Optional["City"]] = relationship()  # nullable one-to-many

    # many-to-many
    # lazy=select prevents `cities` from being auto-joined when we query `settings` (and `users`)
    saved_cities: Mapped[List["City"]] = relationship(
        secondary=settings_cities_association, back_populates="settings", lazy="select"
    )


class City(Base):
    __tablename__ = "cities"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(VARCHAR(length=30))

    # if the gridpoints change, we'll need to make an API call to find the updated gridpoints with these coords
    latitude: Mapped[float] = mapped_column(
        NUMERIC(9, 7, decimal_return_scale=False, asdecimal=False),
        nullable=False,  # set decimal_return_scale to True with postgres
    )
    longitude: Mapped[float] = mapped_column(
        NUMERIC(10, 7, decimal_return_scale=False, asdecimal=False), nullable=False
    )

    # https://www.weather.gov/srh/nwsoffices#
    gridpoint_office: Mapped[str] = mapped_column(CHAR(3), nullable=False)

    # default gridpoints the app will use to get weather for a city. These are created with a lat/long, which
    # will be provided by a third-party API probably
    gridpoint_x: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    gridpoint_y: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    date_created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_modified: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.utc_timestamp()
    )


# TODO:
# Locations table:
# - lat, long cols, higher precision
# - one City, many Locations
#
# SavedLocations table:
# - name col
# - one UserSettings, many SavedCities.SavedLocations
# - foreign-key of SavedLocation to get lat-long
#
# Stored Procedure to use PostGIS to see which Locations are within the same NWS gridpoint, consolidate those records
# - this will allow users to use a mapbox to drop pins on places, name them, and get weather for that exact location.
# - they name these locations and save them. But to keep the number of these reasonable, the stored procedure will cull redundant records
