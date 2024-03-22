import asyncio
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, BigInteger, Integer, String, Text, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.db import engine


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
    selling_price: Mapped[float] = mapped_column(Float, nullable=True)
    predicted_price: Mapped[float] = mapped_column(Float)


class CarsSchemeResponse(BaseModel):
    brand: str
    model: str
    year: int
    km_driven: float
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: Optional[float] = None
    engine: Optional[float] = None
    max_power: Optional[float] = None
    torque: Optional[float] = None
    seats: Optional[int] = None
    max_torque_rpm: Optional[float] = None
    selling_price: Optional[float] = None
    predicted_price: float


class CarsSchemeRequest(BaseModel):
    brand: str
    model: str
    year: int
    km_driven: float
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: Optional[float] = None
    engine: Optional[float] = None
    max_power: Optional[float] = None
    torque: Optional[float] = None
    seats: Optional[int] = None
    max_torque_rpm: Optional[float] = None


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())
