from aiohttp import web
#from .routes_main import routes
#from .routes_api import api
from .routes_app import sub_app
from .routes_appV2 import sub_appV2

"""
async def root_route_handler(request):
    return web.json_response({"status": "alive", "message": "Server is running"})



def web_server():
    web_app = web.Application(client_max_size=500)
    web_app.router.add_get('/', root_route_handler)
    web_app.add_routes(routes)
    web_app.add_subapp('/app', sub_app)
    web_app.add_subapp('/api', api)
    return web_app

"""