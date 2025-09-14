import re
import uuid
import requests


API_HLS = "https://chaturbate.com/get_edge_hls_url_ajax/"

_url_re = re.compile(r"https?://(\w+\.)?chaturbate\.(com|eu)/(?P<username>\w+)")

'''_post_schema = validate.Schema(
    {
        "url": validate.text,
        "room_status": validate.text,
        "success": int
    }
)'''



async def chaturbate_get_streams(url):
    match = _url_re.match(url)
    username = match.group("username")

    CSRFToken = str(uuid.uuid4().hex.upper()[0:32])

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": CSRFToken,
        "X-Requested-With": "XMLHttpRequest",
        "Referer": url,
    }

    cookies = {
        "csrftoken": CSRFToken,
    }

    post_data = "room_slug={0}&bandwidth=high".format(username)

    res = requests.post(API_HLS, headers=headers, cookies=cookies, data=post_data)
    data = res.json()

    #self.logger.info("Stream status: {0}".format(data["room_status"]))
    if (data["success"] is True and data["room_status"] == "public" and data["url"]):
        sStreamURL=  data["url"]
    else:
        print("Error")
    return  sStreamURL