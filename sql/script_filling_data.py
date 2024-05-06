import asyncio
import os
import sys

from sqlalchemy import text
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.db.database import async_session_maker



async def fill_db() -> None:
    os.chdir(os.path.dirname(__file__))

    with open("users.sql") as file:
        sql_script = file.read()
        async with async_session_maker() as session:
            await session.execute(text(sql_script))
            await session.commit()


async def main() -> None:
    await fill_db()


if __name__ == "__main__":
    asyncio.run(main())
