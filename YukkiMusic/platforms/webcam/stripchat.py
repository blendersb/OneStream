import re
import requests
from requests.exceptions import RequestException

# Regular expression for extracting the username from the URL
_url_re = re.compile(r"https?://(\w+\.)?stripchat\.(com|global)/(?P<username>[a-zA-Z0-9_-]+)")

# Validation schema for JSON response
#from streamlink.plugin.api import validate

'''_post_schema = validate.Schema(
    {
        "cam": validate.Schema({
            'streamName': validate.text,
            'viewServers': validate.Schema({'flashphoner-hls': validate.text})
        }),
        "user": validate.Schema({
            'user': validate.Schema({
                'status': validate.text,
                'isLive': bool
            })
        })
    }
)'''

async def get_stripchat_stream_url(url):
    # Extract the username from the URL
    match = _url_re.match(url)
    if not match:
        raise ValueError("Invalid URL format.")
    
    username = match.group("username")
    api_call = f"https://stripchat.com/api/front/v2/models/username/{username}/cam"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": url,
    }

    try:
        # Make the request to the API
        response = requests.get(api_call, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Validate JSON structure using the defined schema
        #data = validate.validate(_post_schema, data)

        # Construct the HLS URL
        #server = f"https://b-hls-21.doppiocdn.com/hls/{data['cam']['streamName']}/master_{data['cam']['streamName']}.m3u8"
        server0 = f"https://b-hls-21.doppiocdn.com/hls/{data['cam']['streamName']}/{data['cam']['streamName']}.m3u8"

        # Check if the stream is live and public
        print(server0)
        if data["user"]["user"]["isLive"] and data["user"]["user"]["status"] == "public":
            # Return the main server stream URL if available, else fallback
            return server0
        else:
            print("The stream is not live or not public.")
            return "The stream is not live or not public."

    except RequestException as e:
        print(f"HTTP request failed: {e}")
    except UnboundLocalError as e:
        print(f"Validation failed: {e}")
    return None

# Example usage:
'''url = "https://stripchat.com/someusername"
stream_url = get_stripchat_stream_url(url)
if stream_url:
     return stream_url
else:
    print("Stream is not available.")
'''