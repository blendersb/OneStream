
import traceback
import math
from aiohttp import web
import config
from pyrogram.file_id import FileId
from aiohttp.http_exceptions import BadStatusLine



from YukkiMusic.core.bot import YukkiBot
from YukkiMusic.core.userbot import multi_clients,req_client
from YukkiMusic.platforms.custom_dl import ByteStreamer
from YukkiMusic.platforms.file_properties import get_file_info,get_name
from YukkiMusic.server.routes_api import fetch_youtube
from YukkiMusic.server.routes_app import sub_app
from YukkiMusic.server.routes_appV2 import sub_appV2

from . import app, userbot


class InvalidHash(Exception):
    message = "Invalid hash"

class FIleNotFound(Exception):
    message = "File not found"



class_cache={}     
async def media_streamer(request: web.Request, db_id: str):
  range_header = request.headers.get("Range", 0)

  #index = min(work_loads, key=work_loads.get)
  #faster_client = multi_clients[index]
  client=app
  #client = await req_client()
  #get_me = await app.get_me()
  #print(db_id,int(config.LOG_GROUP_ID),get_me)
  msg = await client.get_messages(int(config.LOG_GROUP_ID),int(db_id))
  
  #print(msg)
  #tg_connect = ByteStreamer(client['client'])
  tg_connect = ByteStreamer(client)
  #class_cache[client['client']] = tg_connect
  #logging.debug("before calling get_file_properties")
  file_info = get_file_info(msg)
  #file_i = file_info['file']['file_id']
  file_id = FileId.decode(file_info['file']['file_id'])
  #print(file_id)
  #logging.debug("after calling get_file_properties")
  
  file_size = file_info['file']['file_size']

  if range_header:
    from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
    from_bytes = int(from_bytes)
    until_bytes = int(until_bytes) if until_bytes else file_size - 1
  else:
    from_bytes = request.http_range.start or 0
    until_bytes = (request.http_range.stop or file_size) - 1

  if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes
                                                       < from_bytes):
    return web.Response(
        status=416,
        body="416: Range not satisfiable",
        headers={"Content-Range": f"bytes */{file_size}"},
    )

  chunk_size = 512 * 1024
  until_bytes = min(until_bytes, file_size - 1)

  offset = from_bytes - (from_bytes % chunk_size)
  first_part_cut = from_bytes - offset
  last_part_cut = until_bytes % chunk_size + 1

  req_length = until_bytes - from_bytes + 1
  part_count = math.ceil(until_bytes / chunk_size) - math.floor(
      offset / chunk_size)
  body = tg_connect.yield_file(file_id, client, offset, first_part_cut,
                               last_part_cut, part_count, chunk_size)

  mime_type = file_info['file']['mime_type']
  file_name = get_name(msg)
  disposition = "attachment"

  

  # if "video/" in mime_type or "audio/" in mime_type:
  #     disposition = "inline"

  return web.Response(
      status=206 if range_header else 200,
      body=body,
      headers={
          "Content-Type": f"{mime_type}",
          "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
          "Content-Length": str(req_length),
          "Content-Disposition": f'{disposition}; filename="{file_name}"',
          "Accept-Ranges": "bytes",
      },
  )




async def root_route_handler(request):
    return web.json_response({"status": "alive", "message": "Server is running"})

async def render_youtube(request: web.Request):
  try:
    #path = request.match_info["path"]
    return web.Response(text=await fetch_youtube(), content_type='text/html')
  except InvalidHash as e:
    raise web.HTTPForbidden(text=e.message)
  except FIleNotFound as e:
    raise web.HTTPNotFound(text=e.message)
  except (AttributeError, BadStatusLine, ConnectionResetError):
    pass
async def post_method(request: web.Request):

  data = await request.post()
  print(data)
  return web.json_response({
      "status": "ok"
      
  })

async def stream_handler(request: web.Request):
  try:
    path = request.match_info["path"]
    return await media_streamer(request, path)
  except InvalidHash as e:
    raise web.HTTPForbidden(text=e.message)
  except FIleNotFound as e:
    raise web.HTTPNotFound(text=e.message)
  except (AttributeError, BadStatusLine, ConnectionResetError):
    pass
  except Exception as e:
    traceback.print_exc()
    #logging.critical(e.with_traceback(None))
    #logging.debug(traceback.format_exc())
    raise web.HTTPInternalServerError(text=str(e))
 
  
def web_server():
    web_app = web.Application(client_max_size=500)
    web_app.router.add_get('/', root_route_handler)
    web_app.router.add_get('/dl/{path}', stream_handler)
    #web_app.router.add_get('/yt', render_youtube)
    web_app.router.add_get('/post', post_method)
    web_app.add_subapp('/app', sub_app)
    web_app['sub_app'] = sub_app
    web_app.add_subapp('/appV2', sub_appV2)
    web_app['sub_appV2'] = sub_appV2
    
    return web_app