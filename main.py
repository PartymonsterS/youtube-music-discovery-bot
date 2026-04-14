import asyncio

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot import bot, dp
from config import BOT_TOKEN, PORT, WEBHOOK_BASE_URL

from handlers.start import router as start_router
from handlers.help import router as help_router
from handlers.sync import router as sync_router
from handlers.random_liked_music import router as random_liked_music_router
from handlers.playlists import router as playlists_router
from handlers.music_flow import router as music_flow_router
from handlers.admin_settings import router as admin_settings_router
from handlers.community_playlists import router as community_playlists_router


WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"


def register_routers():
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(sync_router)
    dp.include_router(random_liked_music_router)
    dp.include_router(playlists_router)
    dp.include_router(music_flow_router)
    dp.include_router(admin_settings_router)
    dp.include_router(community_playlists_router)


async def on_startup(bot):
    if WEBHOOK_BASE_URL:
        webhook_url = f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}"
        await bot.set_webhook(webhook_url, drop_pending_updates=True)
        print(f"Webhook set to: {webhook_url}")


async def on_shutdown(bot):
    if WEBHOOK_BASE_URL:
        await bot.delete_webhook()
    await bot.session.close()


async def healthcheck(request):
    return web.Response(text="OK")


def create_app():
    app = web.Application()

    app.router.add_get("/", healthcheck)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    return app


async def run_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main():
    register_routers()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    if WEBHOOK_BASE_URL:
        app = create_app()
        web.run_app(app, host="0.0.0.0", port=PORT)
    else:
        asyncio.run(run_polling())


if __name__ == "__main__":
    main()