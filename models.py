import asyncio
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import BigInteger, Integer, String, Text, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from db import engine


class Base(DeclarativeBase):
    pass


class Cars(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String, nullable=True)
    model: Mapped[str] = mapped_column(String, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    km_driven: Mapped[float] = mapped_column(Float, nullable=True)
    fuel: Mapped[str] = mapped_column(String, nullable=True)
    seller_type: Mapped[str] = mapped_column(String, nullable=True)
    transmission: Mapped[str] = mapped_column(String, nullable=True)
    owner: Mapped[str] = mapped_column(String, nullable=True)
    mileage: Mapped[float] = mapped_column(Float, nullable=True)
    engine: Mapped[float] = mapped_column(Float, nullable=True)
    max_power: Mapped[float] = mapped_column(Float, nullable=True)
    torque: Mapped[float] = mapped_column(Float, nullable=True)
    seats: Mapped[int] = mapped_column(Integer, nullable=True)
    max_torque_rpm: Mapped[float] = mapped_column(Float, nullable=True)
    predicted_price: Mapped[float] = mapped_column(Float)


class LogInfo(Base):
    __tablename__ = "log_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    text: Mapped[str] = mapped_column(String, nullable=True)


class CarsScheme(BaseModel):
    brand: str
    model: str
    year: int
    km_driven: float
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: float
    engine: float
    max_power: float
    torque: float
    seats: int
    max_torque_rpm: float

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())
