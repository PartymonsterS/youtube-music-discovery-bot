import asyncio

from bot import bot, dp

from handlers import admin
from handlers.start import router as start_router
from handlers.help import router as help_router
from handlers.sync import router as sync_router
from handlers.random_liked_music import router as random_liked_music_router
from handlers.playlists import router as playlists_router
from handlers.music_flow import router as music_flow_router


async def main():
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(sync_router)
    dp.include_router(random_liked_music_router)
    dp.include_router(playlists_router)
    dp.include_router(music_flow_router)
    dp.include_router(admin.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())