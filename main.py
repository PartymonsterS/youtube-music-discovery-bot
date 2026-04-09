import asyncio

from handlers import admin, client
from bot import bot, dp

async def main():

    dp.include_router(client.router)
    dp.include_router(admin.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())