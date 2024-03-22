import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import pandas as pd
from io import BytesIO
import json

from src.db_manager import Database
from src.models import CarsSchemeRequest

app = FastAPI()


@app.get(path="/")
def root():
    return {"detail": "The service is live"}


@app.get(path="/get_cars")
async def get_db_info(db: Database):
    result = await db.get_all_cars()
    return result


@app.post(path='/predict', summary="Predict")
async def predict_base(db: Database, car: CarsSchemeRequest):
    dct = car.dict()
    df = pd.DataFrame([dct])
    df = await db.make_predictions(df)
    dct['predicted_price'] = df['predicted_price'][0]
    response = dct
    return response


@app.post(path='/predict_by_csv', summary="Predict by csv")
async def predict_by_csv(db: Database, file: UploadFile):
    content = file.file.read()  # считываем байтовое содержимое
    buffer = BytesIO(content)  # создаем буфер типа BytesIO
    df = pd.read_csv(buffer)  # , index_col=0)
    buffer.close()
    pred_df = await db.make_predictions(df)
    pred_df.to_csv('prediction.csv', index=False)
    response = FileResponse(path='prediction.csv', media_type='text/csv', filename='prediction.csv')
    return response


@app.post(path='/predict_by_json', summary="Predict by json")
async def predict_by_json(db: Database, file: UploadFile):
    contents = file.file
    dct = json.load(contents)
    df = pd.DataFrame([dct])
    df = await db.make_predictions(df)
    dct['predicted_price'] = df['predicted_price'][0]
    response = dct
    return response


if __name__ == '__main__':
    uvicorn.run(app="app:app", host='0.0.0.0', port=8000, reload=True)
