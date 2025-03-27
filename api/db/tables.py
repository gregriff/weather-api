from sqlalchemy import (
    UUID,
    Boolean,
    ForeignKey,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(40), unique=True)

    settings_id: Mapped[str] = mapped_column(UUID, ForeignKey("settings.id"))
    settings: Mapped["UserSettings"] = relationship(
        "Settings", back_populates="users", lazy="select"
    )


class UserSettings(Base):
    __tablename__ = "settings"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True)
    favorite_city: Mapped[str] = mapped_column(String(40), unique=False)
    celcius: Mapped[bool] = mapped_column(Boolean, default=False)
