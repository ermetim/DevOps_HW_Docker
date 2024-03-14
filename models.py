import asyncio
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import BigInteger, Integer, String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from db import engine


class Base(DeclarativeBase):
    pass


class TwitchUser(Base):
    __tablename__ = "twitch_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    twitch_user_id: Mapped[int] = mapped_column(BigInteger, default=0, unique=True, nullable=False)
    login: Mapped[str] = mapped_column(String, nullable=True)
    display_name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    email: Mapped[str] = mapped_column(String, nullable=True)
    broadcaster_type: Mapped[str] = mapped_column(String)


class LogInfo(Base):
    __tablename__ = "log_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    text: Mapped[str] = mapped_column(String, nullable=True)


class TwitchUserScheme(BaseModel):
    twitch_user_id: int  # twitch_user_id
    login: str
    display_name: str
    type: str
    description: str
    view_count: int
    broadcaster_type: str
    email: Optional[str] = ""


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())
