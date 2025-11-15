#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
import os
import asyncio
import importlib
import logging
import signal
import sys
from aiohttp import web
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from YukkiMusic import LOGGER, app, userbot
from YukkiMusic.alive import web_server
from YukkiMusic.core.call import Yukki
from YukkiMusic.plugins import ALL_MODULES
from YukkiMusic.utils.database import get_banned_users, get_gbanned

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize event loop
global loop
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

server = web.AppRunner(web_server())

async def init():
    """Initialize the bot and start services."""
    await server.setup()
    await web.TCPSite(server, '0.0.0.0', 7860).start()
    LOGGER("YukkiMusic").info("------------------------------ Web Server Started ------------------------------")

    if not config.STRING1 and not config.STRING2 and not config.STRING3 and not config.STRING4 and not config.STRING5:
        LOGGER("YukkiMusic").error("No Assistant Clients Vars Defined! Exiting Process.")
        return

    if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("YukkiMusic").warning("No Spotify Vars defined. Your bot won't be able to play Spotify queries.")

    await add_banned_users()
    await app.start()

    # Dynamically import all modules
    await import_modules()

    await userbot.start()
    await Yukki.start()

    try:
        await Yukki.stream_call("http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4")
    except NoActiveGroupCall:
        LOGGER("YukkiMusic").error("Please turn on your Logger Group's Voice Call. Make sure you never close/end the voice call.")
        sys.exit(1)
    except Exception as e:
        LOGGER("YukkiMusic").exception("Error starting call: %s", e)

    LOGGER("YukkiMusic").info("Yukki Music Bot Started Successfully")
    await idle()

async def add_banned_users():
    """Add banned users to the global banned list."""
    try:
        gbanned_users = await get_gbanned()
        for user_id in gbanned_users:
            BANNED_USERS.add(user_id)

        banned_users = await get_banned_users()
        for user_id in banned_users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("YukkiMusic").exception("Error adding banned users: %s", e)

async def import_modules():
    """Dynamically import all modules."""
    clean_modules = [m.lstrip(".") for m in ALL_MODULES if isinstance(m, str) and m.strip()]
    for module in clean_modules:
        full_name = f"YukkiMusic.plugins.{module}" if not module.startswith("YukkiMusic.plugins") else module
        try:
            importlib.import_module(full_name)
            LOGGER("YukkiMusic.plugins").info("Imported: %s", full_name)
        except Exception as e:
            LOGGER("YukkiMusic.plugins").exception("Failed importing %s: %s", full_name, e)

async def cleanup():
    """Gracefully stop all running services."""
    LOGGER("YukkiMusic").info("------------------ Stopping Services -----------------")
    
    if server and server.sites:
        LOGGER("YukkiMusic").info("Stopping web server...")
        await server.cleanup()
        LOGGER("YukkiMusic").info("Web server stopped.")
    
    LOGGER("YukkiMusic").info("Stopping clients...")
    if app.is_initialized:
        await app.stop()
        LOGGER("YukkiMusic").info("Main client stopped.")
    await userbot.stop()

    # Cancel any remaining asyncio tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()

    LOGGER("YukkiMusic").info("All tasks cancelled.")
    await asyncio.gather(*tasks, return_exceptions=True)

    if loop.is_running():
        loop.stop()

async def restart_program():
    """Perform a graceful restart of the bot."""
    LOGGER("YukkiMusic").info("------------------ Restarting Program ------------------")
    await cleanup()
    python = sys.executable
    os.execl(python, python, *sys.argv)  # Replace current process

def handle_signal(signum, frame):
    """Handle system signals for restart or termination."""
    restart_signals = [getattr(signal, s) for s in ["SIGHUP", "SIGUSR1", "SIGUSR2"] if hasattr(signal, s)]
    
    if signum in restart_signals:
        LOGGER("YukkiMusic").info(f"Received signal {signum} — performing hot restart...")
        asyncio.run(restart_program())
    elif signum in (signal.SIGINT, signal.SIGTERM):
        LOGGER("YukkiMusic").info(f"Received termination signal ({signum}) — shutting down gracefully...")
        asyncio.run(cleanup())
        sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    for sig_name in ["SIGHUP", "SIGUSR1", "SIGUSR2", "SIGTERM", "SIGINT"]:
        if hasattr(signal, sig_name):
            signal.signal(getattr(signal, sig_name), handle_signal)

    try:
        loop.run_until_complete(init())
    except (KeyboardInterrupt, SystemExit):
        LOGGER("YukkiMusic").info("------------------------ Services Stopped ------------------------")
    except Exception as e:
        LOGGER("YukkiMusic").exception(f"An unexpected error occurred: {e}")
    finally:
        try:
            await cleanup()
            await loop.shutdown_asyncgens()
        except Exception as e:
            LOGGER("YukkiMusic").exception(f"Error during cleanup: {e}")
        finally:
            if not loop.is_closed():
                loop.close()
            LOGGER("YukkiMusic").info("Application closed.")
            sys.exit(0)  # Ensure clean exit
