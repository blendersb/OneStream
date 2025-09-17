from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode
import requests
import re
import json
import asyncio
import aiohttp
from config import PROXY_USER,PROXY_PASS,PROXY_IP,PROXY_PORT
from pytubefix.innertube import InnerTube
from typing import Any, Dict, Optional
#res = requests.get('https://www.youtube.com/')

async def extract_json_tranding(data):
    # Join the list into a single string
    combined_str = ''.join(data)

    # Use regular expression to find the JSON data after 'ytInitialData = '
    match = re.search(r'var ytInitialData\s*=\s*(\{.*\});', combined_str)

    if match:
        json_str = match.group(1)  # Extract the JSON string
        json_str = json_str.encode('utf-8').decode('unicode_escape')
        try:
            # Parse the JSON data
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return None
    else:
        print("No JSON data found.")
        return None
async def search_videos(query):
    searchresult_list=[]
    
    final_query={'search_query':query,'sp':'EgIQAQ%253D%253D','persist_gl':'IN'}
    param=urlencode(final_query)
    url = urlopen(f'https://www.youtube.com/results?{param}').read()
    soup = BeautifulSoup(url, 'lxml')
    allscript = soup.findAll('script')
    text = ''
    for script in allscript:
        if 'var ytInitialData' in str(script.contents):
            text = str(script.contents)
        else:
            continue

    json_data = await extract_json_tranding(text)
    all_search_video = json_data.get('contents', {}).get(
    'twoColumnSearchResultsRenderer',
    {}).get('primaryContents',
            {}).get('sectionListRenderer',
                    {}).get('contents', [])[0].get('itemSectionRenderer',
                                                   {}).get('contents', [])
    
    for video in all_search_video:
        if video.get('videoRenderer', {}):
            if video.get('videoRenderer',{}).get('descriptionSnippet',{}):
                description=video['videoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['videoRenderer']['videoId'],
                "title":video['videoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['videoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['videoRenderer']['publishedTimeText']['simpleText'] if video.get('videoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['videoRenderer']['lengthText']['simpleText'] if video.get('videoRenderer',{}).get('lengthText',{}) else '',
                "views":video['videoRenderer']['viewCountText']['simpleText'] if video.get('videoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['videoRenderer']['shortViewCountText']['simpleText'] if video.get('videoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['videoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('videoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['videoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
        elif video.get('childVideoRenderer', {}):
            if video.get('childVideoRenderer',{}).get('descriptionSnippet',{}):
                description=video['childVideoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['childVideoRenderer']['videoId'],
                "title":video['childVideoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['childVideoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['childVideoRenderer']['publishedTimeText']['simpleText'] if video.get('childVideoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['childVideoRenderer']['lengthText']['simpleText'] if video.get('childVideoRenderer',{}).get('lengthText',{}) else '',
                "views":video['childVideoRenderer']['viewCountText']['simpleText'] if video.get('childVideoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['childVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['childVideoRenderer']['shortViewCountText']['simpleText'] if video.get('childVideoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['childVideoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('childVideoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['childVideoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
        elif video.get('gridVideoRenderer', {}):
            if video.get('gridVideoRenderer',{}).get('descriptionSnippet',{}):
                description=video['gridVideoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['gridVideoRenderer']['videoId'],
                "title":video['gridVideoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['gridVideoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['gridVideoRenderer']['publishedTimeText']['simpleText'] if video.get('gridVideoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['gridVideoRenderer']['lengthText']['simpleText'] if video.get('gridVideoRenderer',{}).get('lengthText',{}) else '',
                "views":video['gridVideoRenderer']['viewCountText']['simpleText'] if video.get('gridVideoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['gridVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['gridVideoRenderer']['shortViewCountText']['simpleText'] if video.get('gridVideoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['gridVideoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('gridVideoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['gridVideoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
    #print(url,searchresult_list)
    return searchresult_list
########################################### extract continuation token from search_videos_with_post_api ###############################


def extract_next_page_token(json_data: Dict[str, Any]) -> Optional[str]:
    """
    Safely extract continuation token from youtube search JSON.
    Returns the token string or None if not present.
    """
    if not isinstance(json_data, dict):
        return None

    contents = (
        json_data.get("contents", {})
                 .get("twoColumnSearchResultsRenderer", {})
                 .get("primaryContents", {})
                 .get("sectionListRenderer", {})
                 .get("contents", [])
    )

    # ensure we have at least 2 items in contents (contents[1] is expected to hold continuation)
    if not isinstance(contents, list) or len(contents) <= 1:
        return None

    second = contents[1]  # safe now
    if not isinstance(second, dict):
        return None

    cont_item = second.get("continuationItemRenderer")
    if not isinstance(cont_item, dict):
        return None

    endpoint = cont_item.get("continuationEndpoint", {})
    if not isinstance(endpoint, dict):
        return None

    # continuationCommand may or may not exist (some formats use different keys),
    # so try common locations defensively.
    command = endpoint.get("continuationCommand", {})
    token = None
    if isinstance(command, dict):
        token = command.get("token")
    if not token:
        # sometimes token may be directly under continuationEndpoint (less common)
        token = endpoint.get("token")

    return token  # either string or None

async def search_videos_with_post_api(query):
    searchresult_list=[]
    
    '''final_query={'search_query':query,'sp':'EgIQAQ%253D%253D','persist_gl':'IN'}
    param=urlencode(final_query)
    url = urlopen(f'https://www.youtube.com/results?{param}').read()
    soup = BeautifulSoup(url, 'lxml')
    allscript = soup.findAll('script')
    text = ''
    for script in allscript:
        if 'var ytInitialData' in str(script.contents):
            text = str(script.contents)
        else:
            continue

    json_data = await extract_json_tranding(text)
    '''
    final_query={
                    "query": query, 
                    "key":"AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
                    "context": {
                        "client": {
                            "hl":"en",
                            "gl":"IN",
                            "clientName": "WEB",
                            "clientVersion": "2.20230728.00.00"
                        }
                    }
                }
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://youtubei.googleapis.com/youtubei/v1/search',
                json=final_query) as response:
            
            json_data= await response.text()
            json_data=json.loads(json_data)
    
    all_search_video = json_data.get('contents', {}).get(
    'twoColumnSearchResultsRenderer',
    {}).get('primaryContents',
            {}).get('sectionListRenderer',
                    {}).get('contents', [])[0].get('itemSectionRenderer',
                                                   {}).get('contents', [])
    
    '''nextPageToken = json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token'] if json_data.get('contents', {}).get(
    'twoColumnSearchResultsRenderer',
    {}).get('primaryContents',
            {}).get('sectionListRenderer',
                    {}).get('contents', [])[1].get('continuationItemRenderer',{}).get('continuationEndpoint',{}).get('continuationCommand',{}).get('token','') else None
    '''
    nextPageToken = extract_next_page_token(json_data)
    


    for video in all_search_video:
        if video.get('videoRenderer', {}):
            if video.get('videoRenderer',{}).get('descriptionSnippet',{}):
                description=video['videoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['videoRenderer']['videoId'],
                "title":video['videoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['videoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['videoRenderer']['publishedTimeText']['simpleText'] if video.get('videoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['videoRenderer']['lengthText']['simpleText'] if video.get('videoRenderer',{}).get('lengthText',{}) else '',
                "views":video['videoRenderer']['viewCountText']['simpleText'] if video.get('videoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['videoRenderer']['shortViewCountText']['simpleText'] if video.get('videoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['videoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('videoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['videoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
        elif video.get('childVideoRenderer', {}):
            if video.get('childVideoRenderer',{}).get('descriptionSnippet',{}):
                description=video['childVideoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['childVideoRenderer']['videoId'],
                "title":video['childVideoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['childVideoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['childVideoRenderer']['publishedTimeText']['simpleText'] if video.get('childVideoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['childVideoRenderer']['lengthText']['simpleText'] if video.get('childVideoRenderer',{}).get('lengthText',{}) else '',
                "views":video['childVideoRenderer']['viewCountText']['simpleText'] if video.get('childVideoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['childVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['childVideoRenderer']['shortViewCountText']['simpleText'] if video.get('childVideoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['childVideoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('childVideoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['childVideoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
        elif video.get('gridVideoRenderer', {}):
            if video.get('gridVideoRenderer',{}).get('descriptionSnippet',{}):
                description=video['gridVideoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['gridVideoRenderer']['videoId'],
                "title":video['gridVideoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['gridVideoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['gridVideoRenderer']['publishedTimeText']['simpleText'] if video.get('gridVideoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['gridVideoRenderer']['lengthText']['simpleText'] if video.get('gridVideoRenderer',{}).get('lengthText',{}) else '',
                "views":video['gridVideoRenderer']['viewCountText']['simpleText'] if video.get('gridVideoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['gridVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['gridVideoRenderer']['shortViewCountText']['simpleText'] if video.get('gridVideoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['gridVideoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('gridVideoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['gridVideoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
    #print(url,searchresult_list)
    return searchresult_list, nextPageToken

async def search_scroll_videos_with_post_api(query):
    searchresult_list=[]
    
    '''final_query={'search_query':query,'sp':'EgIQAQ%253D%253D','persist_gl':'IN'}
    param=urlencode(final_query)
    url = urlopen(f'https://www.youtube.com/results?{param}').read()
    soup = BeautifulSoup(url, 'lxml')
    allscript = soup.findAll('script')
    text = ''
    for script in allscript:
        if 'var ytInitialData' in str(script.contents):
            text = str(script.contents)
        else:
            continue

    json_data = await extract_json_tranding(text)
    '''
    
    final_query={"continuation": query, "key":"AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8", "context": {"client": {"hl":"en", "gl":"IN", "clientName": "WEB", "clientVersion": "2.20230728.00.00"}}}

    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://youtubei.googleapis.com/youtubei/v1/search',
                json=final_query) as response:
            
            json_data= await response.text()
            json_data=json.loads(json_data)
    #return json_data
    all_search_video = json_data.get('onResponseReceivedCommands', [])[0].get(
    'appendContinuationItemsAction',
    {}).get('continuationItems',
            [])[0].get('itemSectionRenderer',
                    {}).get('contents', [])
    

    nextPageToken =json_data['onResponseReceivedCommands'][0]['appendContinuationItemsAction']['continuationItems'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token'] if len(json_data.get('onResponseReceivedCommands', [])) > 0 and json_data.get('onResponseReceivedCommands', [])[0].get(
    'appendContinuationItemsAction',
    {}).get('continuationItems',
            [])[1].get('continuationItemRenderer',{}).get('continuationEndpoint',{}).get('continuationCommand',{}).get('token','') else None
    

    for video in all_search_video:
        if video.get('videoRenderer', {}):
            if video.get('videoRenderer',{}).get('descriptionSnippet',{}):
                description=video['videoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['videoRenderer']['videoId'],
                "title":video['videoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['videoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['videoRenderer']['publishedTimeText']['simpleText'] if video.get('videoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['videoRenderer']['lengthText']['simpleText'] if video.get('videoRenderer',{}).get('lengthText',{}) else '',
                "views":video['videoRenderer']['viewCountText']['simpleText'] if video.get('videoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['videoRenderer']['shortViewCountText']['simpleText'] if video.get('videoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['videoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('videoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['videoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
        elif video.get('childVideoRenderer', {}):
            if video.get('childVideoRenderer',{}).get('descriptionSnippet',{}):
                description=video['childVideoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['childVideoRenderer']['videoId'],
                "title":video['childVideoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['childVideoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['childVideoRenderer']['publishedTimeText']['simpleText'] if video.get('childVideoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['childVideoRenderer']['lengthText']['simpleText'] if video.get('childVideoRenderer',{}).get('lengthText',{}) else '',
                "views":video['childVideoRenderer']['viewCountText']['simpleText'] if video.get('childVideoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['childVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['childVideoRenderer']['shortViewCountText']['simpleText'] if video.get('childVideoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['childVideoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('childVideoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['childVideoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
        elif video.get('gridVideoRenderer', {}):
            if video.get('gridVideoRenderer',{}).get('descriptionSnippet',{}):
                description=video['gridVideoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['gridVideoRenderer']['videoId'],
                "title":video['gridVideoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['gridVideoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['gridVideoRenderer']['publishedTimeText']['simpleText'] if video.get('gridVideoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['gridVideoRenderer']['lengthText']['simpleText'] if video.get('gridVideoRenderer',{}).get('lengthText',{}) else '',
                "views":video['gridVideoRenderer']['viewCountText']['simpleText'] if video.get('gridVideoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['gridVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['gridVideoRenderer']['shortViewCountText']['simpleText'] if video.get('gridVideoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['gridVideoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('gridVideoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['gridVideoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
    #print(url,searchresult_list)
    return searchresult_list, nextPageToken

async def trending_with_post_api(query):
    searchresult_list=[]
    if query=='Now':
        params="6gQJRkVleHBsb3Jl"
        tab_id=0
    if query == 'Music':
        params="4gINGgt5dG1hX2NoYXJ0cw%3D%3D"
        tab_id=1
    elif query == 'Gaming':
        params="4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D"
        tab_id=2
    elif query == 'Movies':
        params="4gIKGgh0cmFpbGVycw%3D%3D"
        tab_id=3
   # params,tab_id = await params_id_return(query)

    final_query={
  "browseId": "FEtrending",
  "params": params,
  "context": {
    "client": {
        "hl":"en",
        "gl":"IN",
      "clientName": "WEB",
      "clientVersion": "2.20230728.00.00"
      
    }
  }
}
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://youtubei.googleapis.com/youtubei/v1/browse',
                json=final_query) as response:
            
            json_data= await response.text()
            json_data=json.loads(json_data)

    
     
    all_search_video = json_data.get('contents', {}).get('twoColumnBrowseResultsRenderer',{}).get('tabs',[])[tab_id].get('tabRenderer',{}).get('content', {}).get('sectionListRenderer',{}).get('contents', [])[0].get('itemSectionRenderer',{}).get('contents', [])[0].get('shelfRenderer',{}).get('content',{}).get('expandedShelfContentsRenderer',{}).get('items',[])
    #.get('twoColumnSearchResultsRenderer',{}).get('tabs',[])
    #.get('sectionListRenderer',{}).get('contents', [])[0].get('itemSectionRenderer',{}).get('contents', [])[0].get('shelfRenderer',{}).get('content',{}).get('expandedShelfContentsRenderer',{}).get('items',[])
    #return all_search_video
    for video in all_search_video:
        if video.get('videoRenderer', {}):
            if video.get('videoRenderer',{}).get('descriptionSnippet',{}):
                description=video['videoRenderer']['descriptionSnippet']['runs'][0]['text']
            else:
                description=''
            details={
                "id":video['videoRenderer']['videoId'],
                "title":video['videoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['videoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['videoRenderer']['publishedTimeText']['simpleText'] if video.get('videoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['videoRenderer']['lengthText']['simpleText'] if video.get('videoRenderer',{}).get('lengthText',{}) else '',
                "views":video['videoRenderer']['viewCountText']['simpleText'] if video.get('videoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['videoRenderer']['shortViewCountText']['simpleText'] if video.get('videoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['videoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('videoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['videoRenderer']['ownerText']['runs'][0]['text']

            }
            searchresult_list.append(details)
    if query == 'Now':
        all_video_Now = json_data.get('contents', {}).get('twoColumnBrowseResultsRenderer',{}).get('tabs',[])[tab_id].get('tabRenderer',{}).get('content', {}).get('sectionListRenderer',{}).get('contents', [])[2].get('itemSectionRenderer',{}).get('contents', [])[0].get('shelfRenderer',{}).get('content',{}).get('expandedShelfContentsRenderer',{}).get('items',[])
        for video in all_video_Now:
            if video.get('videoRenderer', {}):
                if video.get('videoRenderer',{}).get('descriptionSnippet',{}):
                    description=video['videoRenderer']['descriptionSnippet']['runs'][0]['text']
                else:
                    description=''
                details={
                    "id":video['videoRenderer']['videoId'],
                    "title":video['videoRenderer']['title']['runs'][0]['text'],
                    "thumbnails":video['videoRenderer']['thumbnail']['thumbnails'],
                    "description":description,
                    "publishedTime":video['videoRenderer']['publishedTimeText']['simpleText'] if video.get('videoRenderer',{}).get('publishedTimeText',{}) else '' ,
                    "length":video['videoRenderer']['lengthText']['simpleText'] if video.get('videoRenderer',{}).get('lengthText',{}) else '',
                    "views":video['videoRenderer']['viewCountText']['simpleText'] if video.get('videoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                    "url":f"https://www.youtube.com{video['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                    "short_views":video['videoRenderer']['shortViewCountText']['simpleText'] if video.get('videoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                    "channelThumbnail":video['videoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('videoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                    "channel":video['videoRenderer']['ownerText']['runs'][0]['text']

                }
                searchresult_list.append(details)
    #print(url,searchresult_list)
    return searchresult_list




async def tranding_videos():
    tranding_list=[]
    url = urlopen('https://www.youtube.com/feed/trending/?persist_gl=1&gl=IN').read()
    soup = BeautifulSoup(url, 'lxml')
    allscript = soup.findAll('script')
    text = ''
    for script in allscript:
        if 'var ytInitialData' in str(script.contents):
            text = str(script.contents)
        else:
            continue

    json_data = await extract_json_tranding(text)
    
    all_video = json_data.get('contents', {}).get(
        'twoColumnBrowseResultsRenderer',
        {}).get('tabs', [])[0].get('tabRenderer', {}).get('content', {}).get(
            'sectionListRenderer',
            {}).get('contents', [])[3].get('itemSectionRenderer', {}).get(
                'contents',
                [])[0].get('shelfRenderer',
                        {}).get('content',
                                {}).get('expandedShelfContentsRenderer',
                                        {}).get('items', [])
    #"descriptions":video['videoRenderer']['descriptionSnippet']['runs'][0]['text'],
    '''nextPageToken = json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token'] if json_data.get('contents', {}).get(
    'twoColumnSearchResultsRenderer',
    {}).get('primaryContents',
            {}).get('sectionListRenderer',
                    {}).get('contents', [])[1].get('continuationItemRenderer',{}).get('continuationEndpoint',{}).get('continuationCommand',{}).get('token','') else None
    '''



    for video in all_video:
        if video.get('videoRenderer',{}).get('descriptionSnippet',{}):
            description=video['videoRenderer']['descriptionSnippet']['runs'][0]['text']
        else:
            description=''
        details={
                "id":video['videoRenderer']['videoId'],
                "title":video['videoRenderer']['title']['runs'][0]['text'],
                "thumbnails":video['videoRenderer']['thumbnail']['thumbnails'],
                "description":description,
                "publishedTime":video['videoRenderer']['publishedTimeText']['simpleText'] if video.get('videoRenderer',{}).get('publishedTimeText',{}) else '' ,
                "length":video['videoRenderer']['lengthText']['simpleText'] if video.get('videoRenderer',{}).get('lengthText',{}) else '',
                "views":video['videoRenderer']['viewCountText']['simpleText'] if video.get('videoRenderer',{}).get('viewCountText',{}).get('simpleText','') else '',
                "url":f"https://www.youtube.com{video['videoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
                "short_views":video['videoRenderer']['shortViewCountText']['simpleText'] if video.get('videoRenderer',{}).get('shortViewCountText',{}).get('simpleText','') else '',
                "channelThumbnail":video['videoRenderer']['channelThumbnailSupportedRenderers']['channelThumbnailWithLinkRenderer']['thumbnail']['thumbnails'][0]['url'] if video.get('videoRenderer',{}).get('channelThumbnailSupportedRenderers',{}) else '',
                "channel":video['videoRenderer']['ownerText']['runs'][0]['text']

            }
        tranding_list.append(details)
    #print(tranding_list)
    return tranding_list

#####-------------RETURN VIDEO LIST WITH STREAMING URL BY VIDEO ID------######
async def search_player_data_with_post_api(query):
    searchresult_list=[]
    
    
    '''final_query={
                    "context":{
                        "client":{"hl":"en",
                                  "gl":"IN",
                                  "deviceMake":"",
                                  "deviceModel":"",
                                  "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0,gzip(gfe)",
                                  "clientName":"IOS",
                                  "clientVersion":"19.16.3",
                                  "screenPixelDensity":1,
                                  "timeZone":"Asia/Kolkata",
                                  "browserName":"Firefox",
                                  "browserVersion":"132.0",
                                  "acceptHeader":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                  "deviceExperimentId":"ChxOelF6TkRNNU1UTTJPRE01T0RrNE9EZzVNQT09EI-HsbkGGI-HsbkG",
                                  "screenWidthPoints":1534,
                                  "screenHeightPoints":334,
                                  "utcOffsetMinutes":330,
                                  "clientScreen":"WATCH",
                                  "mainAppWebInfo":{
                                      "pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_UNKNOWN",
                                      "webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":"false"
                                      }
                                },
                                "user":{"lockedSafetyMode":"false"},
                                "request":{"useSsl":"true","internalExperimentFlags":[],"consistencyTokenJars":[]},
                                "clickTracking":{"clickTrackingParams":"CNQCENwwIhMI1emaz7LJiQMVN-lMAh3IOCkMMgpnLWhpZ2gtcmVjWg9GRXdoYXRfdG9fd2F0Y2iaAQYQjh4YngE="}
                            },
                            "videoId":query,
                            "params":"YAHIAQE%3D",
                            "playbackContext":{
                                "contentPlaybackContext":{
                                    "vis":5,
                                    "splay":"false",
                                    "autoCaptionsDefaultOn":"false",
                                    "autonavState":"STATE_NONE",
                                    "html5Preference":"HTML5_PREF_WANTS",
                                    "signatureTimestamp":20032,
                                    "autoplay":"true",
                                    "autonav":"true",
                                    "referer":"https://www.youtube.com/",
                                    "lactMilliseconds":"-1",
                                    "watchAmbientModeContext":{
                                        "hasShownAmbientMode":"true","watchAmbientModeEnabled":"true"}
                                        }
                                    },
                                    "racyCheckOk":"false",
                                    "contentCheckOk":"false"
                                    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://youtubei.googleapis.com/youtubei/v1/player',
                json=final_query,proxy=f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_IP}:{PROXY_PORT}",) as response:
            
            json_data= await response.text()
            json_data=json.loads(json_data)
    #return json_data
    innertube = InnerTube(client='WEB')  # You can use other clients like ANDROID_VR, WEB, etc.
    
    # Then, fetch player info using a YouTube video ID
    video_id = query  # Example video ID
    player_info = innertube.player(video_id)
    print(player_info)
    json_data=json.loads(player_info)
    all_formats_video = json_data.get('streamingData', {}).get(
    'formats',
    [])
    all_adaptive_formats_video = json_data.get('streamingData', {}).get(
    'adaptiveFormats',
    [])
    videodetails = json_data.get('videoDetails', {})


    for video in all_formats_video:
        
        searchresult_list.append(video)
    for video in all_adaptive_formats_video:
        
        searchresult_list.append(video)'''
    final_query={"url":"https://www.youtube.com/watch?v="+query}
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://www.clipto.com/api/youtube',
                json=final_query) as response:
            
            json_data= await response.text()
            json_data=json.loads(json_data)
    #return json_data
    #all_formats_video = json_data.get('streamingData', {}).get(
    #'formats',
    #[])
    all_adaptive_formats_video = json_data.get('medias', [])
    #print(all_adaptive_formats_video)
    #videodetails = json_data.get('videoDetails', {})


    '''for video in all_formats_video:
        
        searchresult_list.append(video)
    for video in all_adaptive_formats_video:
        
        searchresult_list.append(video)
        
    #print(url,searchresult_list)'''
    return all_adaptive_formats_video
        
    
    #return searchresult_list, videodetails
    '''   video details content JSON DATA {} with key:value
    demo data 
    {
        "videoId": "k3g_WjLCsXM",
        "title": "Sajni (Song): Arijit Singh, Ram Sampath | Laapataa Ladies |  Aamir Khan Productions",
        "lengthSeconds": "146",
        "keywords": [
            "sajni laapata ladies",
            "sajni laapataa ladies",
            "sajni"
        ],
        "channelId": "UCq-Fj5jknLsUf-MWSy4_brA",
        "isOwnerViewing": false,
        "shortDescription": "Presenting the Song \"Sajni\" from the upcoming film Laapataa Ladies. Sung by Arijit Singh, Composed by Ram Sampath and Penned by Prashant Pandey.\n\n#LaapataaLadies #Sajni #ArijitSingh #RamSampath\n\nJio Studios Presents \nAamir Khan Productions \"LAAPATAA LADIES\" \n\n♪Full Song Available on♪ \nJioSaavn: https://bit.ly/3SV0n0w\nSpotify: https://bit.ly/3wgICzV\nHungama: https://bit.ly/499FkNy\nApple Music: https://bit.ly/3SEqRlL\nAmazon Prime Music: https://bit.ly/3Uxi1Zv\nWynk: https://bit.ly/3uwyX7O\nYouTube Music: https://bit.ly/4bzkV5R\n\nSong Credits:\nSong Name: Sajni\nComposed By : Ram Sampath\nLyricist : Prashant Pandey\nSinger : Arijit Singh\nMusic Arranged & Produced by : Ram Sampath\nMusic Supervisor : Vrashal Chavan\nRecorded & Mixed at Omgrown Music, Mumbai by Amey Wadibhasme\nMastered by Gethin John at Hafod Mastering\nVocal Recordist : Sukanto Singha\nVocal Editor : Prithviraj Sarkar\nMusic Label: T-Series\n\nFilm Credits: \nDirected by Kiran Rao \nProduced by Aamir Khan, Kiran Rao & Jyoti Deshpande\nStarring : Nitanshi Goel, Pratibha Ranta, Sparsh Shrivastava, Ravi Kishan and Chhaya Kadam\nCo Stars : Bhaskar Jha, Durgesh Kumar, Geeta Aggarwal, Pankaj Sharma, Rachna Gupta, Abeer Jain, Kirti Jain, Daood Hussain, Pranjal Pateriya, Samarth Mohar, Satendra Soni, Ravi Kapadiya, Kishore Soni. \nOriginal Story : Biplab Goswami \nScreenplay & Dialogues : Sneha Desai \nAdditional Dialogues : Divyanidhi Sharma \nMusic : Ram Sampath \nLyricists : Swanand Kirkire, Prashant Pandey, Divyanidhi Sharma \nSingers: Shreya Ghoshal, Arijit Singh, Sukhwinder Singh, Sona Mohapatra\nDirector of Photography : Vikash Nowlakha\nEditor : Jabeen Merchant \nProduction Designer : Vikram Singh \nCostume Designer : Darshan Jalan \nCasting : Romil Jain \nSound Designer : Ayush Ahuja \nProduction Sound Mixer : Ravi Dev Singh \nMake Up Designer : Kamlesh Shinde \nHair Designer : Joyce Fernandez \n1st Assistant Director : Rakesh E. Nair \nLine Producer : Jaspal Dogra \nScript Supervisor : Mandira Roy \nDialect Coach : Sonu Anand \nDirector's Assistant : Pooja Kumar \nColorist : Michele Ricossa \nVisual Effects Studio : SM Rolling \nVFX DI Studio : Prasad Labs \nVisual Promotions : Just Right Studioz NX \nAKP Finance Team : Sharada Harihar, Aditya Shah, Huzvak Batliwala, Pankti Mehta, Tejasvi Gurav, Manisha Abhyankar\nFinancial Advisor : Bimal Parekh & Co \nExecutive Producers : Antara Banerjee & Naved Farooqui \nCo-Producers : B. Shrinivas Rao & Tanaji Dasgupta \n\nDownload Song Beat: https://bit.ly/3Cjh24R \n\n___________________________________\nEnjoy & stay connected with us!\n👉 Subscribe to T-Series: https://youtube.com/tseries\n👉 Like us on Facebook: https://www.facebook.com/tseriesmusic\n👉 Follow us on X: https://twitter.com/tseries\n👉 Follow us on Instagram: https://instagram.com/tseries.official",
        "isCrawlable": true,
        "thumbnail": {
            "thumbnails": [
                {
                    "url": "https://i.ytimg.com/vi/k3g_WjLCsXM/default.jpg",
                    "width": 120,
                    "height": 90
                },
                {
                    "url": "https://i.ytimg.com/vi/k3g_WjLCsXM/mqdefault.jpg",
                    "width": 320,
                    "height": 180
                },
                {
                    "url": "https://i.ytimg.com/vi/k3g_WjLCsXM/hqdefault.jpg",
                    "width": 480,
                    "height": 360
                },
                {
                    "url": "https://i.ytimg.com/vi/k3g_WjLCsXM/sddefault.jpg",
                    "width": 640,
                    "height": 480
                }
            ]
        },
        "allowRatings": true,
        "viewCount": "70761818",
        "author": "T-Series",
        "isPrivate": false,
        "isUnpluggedCorpus": false,
        "isLiveContent": false
    }'''

    

'''
async def main():
    result= await trending_with_post_api('Movies')
    print(result)
    #result=str(result)
    #print(result.encode('utf-8'))  # Print the result

# Run the main function in the event loop
if __name__ == "__main__":
    asyncio.run(main())
    '''