import re
import requests

from datetime import datetime

STREAM_INFO = "https://www.cam4.com/rest/v1.0/profile/{0}/streamInfo"
INFO_URL = "https://www.cam4.com/rest/v1.0/search/performer/{0}"
PROFILE_URL = "https://www.cam4.com/rest/v1.0/profile/{0}/info"

_url_re = re.compile(r"https?://(\w+\.)?cam4\.(com|eu)/(?P<username>\w+)")


async def cam4_get_streams(url):
    match = _url_re.match(url)
    username = match.group("username")

    res = requests.get(INFO_URL.format(username))
    res.raise_for_status()
    data = res.json()

    online = data["online"]
    
    if online:
        
        res = requests.get(STREAM_INFO.format(username))
        res.raise_for_status()
        data = res.json()
        if data["canUseCDN"]:
            sStreamURL = data["cdnURL"]
            
        else:
            print("Access: private")
    return sStreamURL

