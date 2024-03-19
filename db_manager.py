from typing import Optional, Annotated

from fastapi import Depends, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db_session
from models import Cars, CarsScheme, LogInfo
from functions import DataPreprocessing



class RelationalManager:
    db: AsyncSession = None

    async def connect_to_database(self, session: Optional[AsyncSession] = None) -> None:
        if session is not None:
            self.db = session
            return
        self.db = await get_db_session()

    async def close_database_connection(self) -> None:
        await self.db.close()

    async def get_all_cars(self) -> list[CarsScheme]:
        result = await self.db.execute(
            select(Cars)  # SELECT * FROM table;
        )
        cars = result.scalars().all()  # list[TwitchUser]
        return [CarsScheme(**car.__dict__) for car in cars]

    async def make_predictions(self, df) -> None:


        preprocessing = DataPreprocessing(models_folder="models")
        X_test, y_test = preprocessing.run_test(df)

        prediction, score = preprocessing.model_predict(X_test)
        df['predicted_price'] = prediction

        for _, row in df.iterrows():
            car = Cars(
                brand=df['brand'],
                model=df['model'],
                year=df['year'],
                km_driven=df['km_driven'],
                fuel=df['fuel'],
                seller_type=df['seller_type'],
                transmission=df['transmission'],
                owner=df['owner'],
                mileage=df['mileage'],
                engine=df['engine'],
                max_power=df['max_power'],
                torque=df['torque'],
                seats=df['seats'],
                max_torque_rpm=df['max_torque_rpm'],
                predicted_price=df['predicted_price'],
            )
            self.db.add(car)
        await self.db.commit()
        return df

async def get_pdb() -> RelationalManager:
    manager = RelationalManager()
    try:
        await manager.connect_to_database()
        yield manager
    finally:
        await manager.close_database_connection()


Database = Annotated[RelationalManager, Depends(get_pdb)]
