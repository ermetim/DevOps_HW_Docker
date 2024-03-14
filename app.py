import uvicorn
from fastapi import FastAPI, Request
from models import TwitchUserScheme
from db_manager import Database

app = FastAPI()


@app.get("/")
def greet():
    return {"detail": "success"}


@app.get("/users")
async def get_db_info(db: Database):
    result = await db.get_all_user()
    return {"success": result}


@app.post("/users")
async def create_user(db: Database, user: TwitchUserScheme):
    result = await db.add_user(user)
    return {"success": True}


@app.get("/do")
async def do_something(db: Database, request: Request):
    await db.track_user(request.headers['user-agent'])
    await db.get_tracks()
    return {"message": "we have stolen your info"}


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)
