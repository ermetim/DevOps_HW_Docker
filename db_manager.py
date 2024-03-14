from typing import Optional, Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db_session
from models import TwitchUser, TwitchUserScheme, LogInfo


class RelationalManager:
    db: AsyncSession = None

    async def connect_to_database(self, session: Optional[AsyncSession] = None) -> None:
        if session is not None:
            self.db = session
            return
        self.db = await get_db_session()

    async def close_database_connection(self) -> None:
        await self.db.close()

    async def get_all_user(self) -> list[TwitchUserScheme]:
        result = await self.db.execute(
            select(TwitchUser)  # SELECT * FROM twitch_users;
        )
        users = result.scalars().all()  # list[TwitchUser]
        return [TwitchUserScheme(**user.__dict__) for user in users]

    async def add_user(self, user: TwitchUserScheme) -> None:
        user = TwitchUser(
            twitch_user_id=user.twitch_user_id,
            login=user.login,
            display_name=user.display_name,
            type=user.type,
            description=user.description,
            view_count=user.view_count,
            email=user.email,
            broadcaster_type=user.email
        )
        self.db.add(user)
        await self.db.commit()

    async def track_user(self, data: str) -> None:
        log_info = LogInfo(
            text=data
        )
        self.db.add(log_info)
        await self.db.commit()

    async def get_tracks(self):
        result = await self.db.execute(
            select(LogInfo)  # SELECT * FROM twitch_users;
        )
        for el in result.scalars().all():
            print(el.created_at, '---', el.text)


async def get_pdb() -> RelationalManager:
    manager = RelationalManager()
    try:
        await manager.connect_to_database()
        yield manager
    finally:
        await manager.close_database_connection()


Database = Annotated[RelationalManager, Depends(get_pdb)]