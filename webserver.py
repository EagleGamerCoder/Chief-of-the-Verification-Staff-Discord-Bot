'''

info

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import os
import asyncio

from aiohttp import web

# Modules


# ------------------------------------------------------------ VARIABLES ------------------------------------------------------------

runner = None

# ------------------------------------------------------------ FUNCTIONS ------------------------------------------------------------

async def start_webserver() -> None:
    app = web.Application()

    async def handle(request):
        return web.Response(text="Bot is running")

    app.router.add_get("/", handle)

    global runner
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()
    print(f"[SETUP] Web server listening on port {port}")



async def close_webserver():
    global runner
    if runner:
        await runner.cleanup()
        runner = None

        

def handle_web_result(task):
    try:
        exc = task.exception()
        if exc:
            print(f"[WEB ERROR] {exc}")
    except asyncio.CancelledError:
        print("[WEB] Task cancelled")