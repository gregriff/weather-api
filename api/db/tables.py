# Declarative code that generates RDBMS-agnostic DDL
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import Index
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
saved_cities_association = Table(
    "saved_cities",
    Base.metadata,
    Column("settings_id", ForeignKey("settings.user_id"), primary_key=True, index=True),
    Column("city_id", ForeignKey("locations.id"), primary_key=True, index=True),
    Column("state", VARCHAR(20)),
    Column("date_created", DateTime, default=func.now()),
    Column("last_modified", DateTime, onupdate=func.utc_timestamp()),
)
saved_locations_association = Table(
    "saved_locations",
    Base.metadata,
    Column("settings_id", ForeignKey("settings.user_id"), primary_key=True, index=True),
    Column("location_id", ForeignKey("locations.id"), primary_key=True, index=True),
    Column("description", VARCHAR(50)),
    Column("color", VARCHAR(7)),  # hex
    Column("date_created", DateTime, default=func.now()),
    Column("last_modified", DateTime, onupdate=func.utc_timestamp()),
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
    settings: Mapped["UserSetting"] = relationship(
        "Settings",
        back_populates="user",
    )


class UserSetting(Base):
    __tablename__ = "settings"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), primary_key=True, index=True
    )

    # there will be a use for these at some point in the list view page
    favorite_city_id: Mapped[str] = mapped_column(
        ForeignKey("locations.id"), nullable=True, index=True
    )
    favorite_location_id: Mapped[str] = mapped_column(
        ForeignKey("locations.id"), nullable=True, index=True
    )

    # used to fetch weather data for last-known location of user as soon as app loads
    last_known_gridpoint_office: Mapped[str] = mapped_column(CHAR(3))
    last_known_gridpoint_x: Mapped[int] = mapped_column(SmallInteger)
    last_known_gridpoint_y: Mapped[int] = mapped_column(SmallInteger)

    # actual settings
    metric: Mapped[bool] = mapped_column(Boolean, default=False)
    military_time: Mapped[bool] = mapped_column(Boolean, default=False)

    date_created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_modified: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.utc_timestamp()
    )

    # ORM-specific declarations and relationships
    user: Mapped["User"] = relationship(back_populates="settings")
    favorite_city: Mapped[Optional["Location"]] = relationship()  # nullable one-to-many
    favorite_location: Mapped[Optional["Location"]] = relationship()

    # many-to-many
    # lazy=select prevents `cities` from being auto-joined when we query `settings` (and `users`)
    saved_cities: Mapped[List["Location"]] = relationship(
        secondary=saved_cities_association, back_populates="settings", lazy="select"
    )
    saved_locations: Mapped[List["Location"]] = relationship(
        secondary=saved_locations_association, back_populates="settings", lazy="select"
    )


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True)
    is_city: Mapped[bool] = mapped_column(Boolean, nullable=False)
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


Index("ix_locations_is_city_id_composite", Location.is_city, Location.id)
