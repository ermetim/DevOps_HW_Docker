from typing import Optional, Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db_session
from src.models import Cars, CarsSchemeResponse
from src.functions import DataPreprocessing


class RelationalManager:
    db: AsyncSession = None


    async def connect_to_database(self, session: Optional[AsyncSession] = None) -> None:
        if session is not None:
            self.db = session
            return
        self.db = await get_db_session()


    async def close_database_connection(self) -> None:
        await self.db.close()


    async def get_all_cars(self) -> list[CarsSchemeResponse]:
        result = await self.db.execute(
            select(Cars)  # SELECT * FROM table;
        )
        cars = result.scalars().all()  # list[cars]
        return [CarsSchemeResponse(**car.__dict__) for car in cars]


    async def make_predictions(self, df) -> None:

        preprocessing = DataPreprocessing(models_folder="models")
        X_test, y_test = preprocessing.run_test(df)

        prediction, score = preprocessing.model_predict(X_test)

        if 'selling_price' not in df.columns:
            df['selling_price'] = None

        df['predicted_price'] = prediction

        for index, row in df.iterrows():
            car = Cars(**row)  # Создаем объект Cars из данных строки DataFrame
            self.db.add(car)  # Добавляем объект в сессию
        await self.db.commit()  # Сохраняем изменения в базе данных
        return df


async def get_pdb() -> RelationalManager:
    manager = RelationalManager()
    try:
        await manager.connect_to_database()
        yield manager
    finally:
        await manager.close_database_connection()


Database = Annotated[RelationalManager, Depends(get_pdb)]
