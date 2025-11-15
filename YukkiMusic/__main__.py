import asyncio
import logging
import sys
import signal
from pyrogram import idle
from aiohttp import web
from YukkiMusic import LOGGER, app, userbot
from YukkiMusic.alive import web_server
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import get_banned_users, get_gbanned

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()

server = web.AppRunner(web_server())

async def init():
    await server.setup()
    await web.TCPSite(server, '0.0.0.0', 7860).start()
    print("------------------------------ Web Server Started ------------------------------")
    
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("YukkiMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return

    if (
        not config.SPOTIFY_CLIENT_ID
        and not config.SPOTIFY_CLIENT_SECRET
    ):
        LOGGER("YukkiMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play Spotify queries."
        )

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    
    await app.start()
    await userbot.start()
    await Yukki.start()
    
    try:
        await Yukki.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("YukkiMusic").error(
            "[ERROR] - \n\nPlease turn on your Logger Group's Voice Call. Make sure you never close/end voice call in your log group"
        )
        sys.exit()
    except Exception as e:
        print(e)
    
    LOGGER("YukkiMusic").info("Yukki Music Bot Started Successfully")
    await idle()

async def cleanup():
    """Gracefully stop all running services."""
    print("\n------------------ Stopping Services -----------------")
    if server and server.sites:
        print("Stopping web server...")
        await server.cleanup()
        print("Web server stopped.")

    print("Stopping clients...")
    if app.is_initialized:
        await app.stop()
        print("Main client stopped.")
        print("User bot stopped.")
        await userbot.stop()
    
    # Stop all asyncio tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()  
    
    print("All tasks cancelled.")
    await asyncio.gather(*tasks, return_exceptions=True)
    if loop.is_running():
        loop.stop()

async def restart_program():
    """Perform a graceful restart."""
    print("\n------------------ Restarting Program ------------------")
    await cleanup()
    python = sys.executable
    os.execl(python, python, *sys.argv)  # Replace current process

def handle_signal(signum, frame):
    restart_signals = [getattr(signal, s) for s in ["SIGHUP", "SIGUSR1", "SIGUSR2"] if hasattr(signal, s)]
    if signum in restart_signals:
        logging.info(f"Received signal {signum} — performing hot restart...")
        asyncio.ensure_future(restart_program())
    elif signum in (signal.SIGINT, signal.SIGTERM):
        logging.info(f"Received termination signal ({signum}) — shutting down gracefully...")
        asyncio.ensure_future(cleanup())
        sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    for sig_name in ["SIGHUP", "SIGUSR1", "SIGUSR2", "SIGTERM", "SIGINT"]:
        if hasattr(signal, sig_name):
            signal.signal(getattr(signal, sig_name), handle_signal)

    try:
        loop.run_until_complete(init())  # Run the main initialization
    except (KeyboardInterrupt, SystemExit):
        print("------------------------ Services Stopped ------------------------")
    except Exception as e:
        LOGGER("YukkiMusic").info(f"Stopping Yukki Music Bot! GoodBye--{e}")
        print(e)
    finally:
        # Run cleanup asynchronously within the running event loop
        asyncio.ensure_future(cleanup())
