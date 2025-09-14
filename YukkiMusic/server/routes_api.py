import aiohttp
import jinja2
import urllib.parse
import argparse
from aiohttp import web
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
parser = argparse.ArgumentParser()
parser.add_argument('--q', help='Search term', default='Google')
parser.add_argument('--max-results', help='Max results', default=25)
args = parser.parse_args()

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyAJB2yzah87l58QCNUFrYOrzu_5I7RFQZY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

async def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q='galpo mirer thek',
    part='id,snippet',
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  #search_result['snippet']['title'],
  #search_result['id']['videoId']
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append(search_result['snippet'])
    elif search_result['id']['kind'] == 'youtube#channel':
      channels.append('%s (%s)' % (search_result['snippet']['title'],
                                   search_result['id']['channelId']))
    elif search_result['id']['kind'] == 'youtube#playlist':
      playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['playlistId']))
    #print(videos)

  return  videos,playlists,channels



  

async def fetch_youtube():

    try:
        videos, playlist, channels = await youtube_search(args)
    except HttpError :
        print('e.resp.status, e.content')
    #r=json.dumps(videos)
    #loaded_r=json.loads(r)
    template_file = "YukkiMusic/server/templates/youtube.html"
    with open(template_file) as f:
        template = jinja2.Template(f.read())

    return template.render()
    #return aiohttp.web.HTTPFound("YukkiMusic/server/templates/youtube.html")
    #return template.render()


