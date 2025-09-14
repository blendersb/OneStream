'''import json
import yt_dlp

URL = 'https://www.youtube.com/watch?v=hxMNYkLN7tI'

# ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    # ℹ️ ydl.sanitize_info makes the info json-serializable
    inf=json.dumps(info)
    print(inf.encode("utf-8"))
    #print(json.dumps(ydl.sanitize_info(info)))'''
import aiohttp
import asyncio
import re
import json
import subprocess
def run_ffmpeg_command(command):
    # Run the command using subprocess and print the output in real time
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1
    )

    # Print stdout and stderr in real time
    for line in process.stdout:
        print(line, end='')

    for line in process.stderr:
        print(line, end='')

    # Wait for the process to complete and get the return code
    process.wait()
    if process.returncode == 0:
        print("FFmpeg process completed successfully.")
    else:
        print(f"FFmpeg process failed with return code {process.returncode}.")

# Example FFmpeg command (modify as needed)
ffmpeg_command = [
    "ffmpeg", "-i", "https://rr2---sn-a5msenl7.googlevideo.com/videoplayback?expire=1731406559&ei=f9YyZ7eMBvrEsfIP8KiGOQ&ip=167.160.180.203&id=o-AGYqnJbekKH-AerZwX-xCnG-pA4zxGT9AZ-mCD2kAk82&itag=139&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1731384959%2C&mh=mb&mm=31%2C26&mn=sn-a5msenl7%2Csn-o097znzr&ms=au%2Conr&mv=m&mvi=2&pl=24&rms=au%2Cau&initcwndbps=815000&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=552165&dur=90.372&lmt=1731208314415603&mt=1731384352&fvip=3&keepalive=yes&fexp=51299154%2C51312688%2C51326932&c=IOS&txp=5532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRAIgCH234H0ybgNxvMcAfaqo8FwuAdG1jLM97ZfN4QojBkoCIE6l21dd7wOu5StL2xFU-0xkYaRCUdOpAc4jrzErxjwJ&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRQIhAKkPzX5PuEGEGSW-DQJ3oGWPdPzkQikgrgOWnOYKUmMAAiBPrlzIPIGazRnVq7LJbDlPPLfpBADxZ51mqEHwO12J0g%3D%3D", "-acodec", "libmp3lame", "output_video.mp3"
]

# Run the FFmpeg command and print the log



async def main():
    '''if(proxy_i[6]=='yes'):
        http="https"
    else:
        http="http"'''
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://youtubei.googleapis.com/youtubei/v1/player/',
                #proxy=f'{http}://{proxy_i[0]}:{proxy_i[1]}',
                #proxy="tcp://147.135.15.16:443",
                proxy="http://qihnryee:g2hsfjzxpu6j@167.160.180.203:6754",
                json={
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
                            "videoId":"fJHPpifqPp0",
                            "params":"YAHIAQE%3D",
                            "playbackContext":{
                                "contentPlaybackContext":{
                                    "currentUrl":"/watch?v=fJHPpifqPp0&pp=YAHIAQE%3D",
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
                                    }) as response:
           
            json_data = await response.text()
            #json_data = json.loads(json_data)
            print(json_data)
            #run_ffmpeg_command(ffmpeg_command)


            #print(json_data.get('streamingData', {}).get('adaptiveFormats',{}))
            

'''number_of_requests = 10
length = len(proxy_list)
for i in range(number_of_requests):
    index = i % length'''
asyncio.run(main())