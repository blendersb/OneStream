import requests
session = requests.Session()
# URL of the form action
url = "https://usproxy.vpnbook.com/includes/process.php?action=update"
#url="https://www.youtubeunblocked.live/server"
# Form data to be sent
form_data = {
    #"csrf":"RXFOUlV0ZjFxdHg5L1VGd1ZrazRKUmxldmpjdGNpSUhXTmg0R2c4K1l6dDRrZkYzQm1NNVh3UzVTOG1kTXgwdHhZcWJNK29vaUk4amFKUHR0cTBMVG4xeXA4eXEvT0hBbTV3ekpBN0lFWWs9",
    "u": "https://rr2---sn-a5mlrnlz.googlevideo.com/videoplayback?expire=1731428343&ei=lyszZ6r0EeuosfIP5IKwiQM&ip=167.160.180.203&id=o-AG05BEzZGzNoyR7e8p8-MZUjJq7v_rsbCRg7hgLt7YKh&itag=139&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&met=1731406743%2C&mh=eG&mm=31%2C26&mn=sn-a5mlrnlz%2Csn-o097znss&ms=au%2Conr&mv=m&mvi=2&pl=24&rms=au%2Cau&initcwndbps=835000&vprv=1&svpuc=1&mime=audio%2Fmp4&rqh=1&gir=yes&clen=735156&dur=120.418&lmt=1731352646377859&mt=1731406637&fvip=2&keepalive=yes&fexp=51299154%2C51312688%2C51326932&c=IOS&txp=4532434&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cvprv%2Csvpuc%2Cmime%2Crqh%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRgIhAMs5WBHg8A-r0-VoEAYJ91DLY4vhcsUB03SNBT4GK7_UAiEAlkNkA1175U0JzUIUUknDJZ-JspfjXMfxhzCtbc2PDzU%3D&lsparams=met%2Cmh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Crms%2Cinitcwndbps&lsig=AGluJ3MwRAIgB9bWPB61A1HPf7Axc9WuvX3P_IzkODTkC3WpUVlX7BECICLQfdiPvGhdjGUXe7mM3Y7p0N36JjMe-_BCIwQlYyK5"  # Replace with the value you want to submit
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

# Send the POST request using the session with custom headers
response = session.post(url, data=form_data, headers=headers, allow_redirects=False)

# Check for the 'Location' header in the response
redirect_url = response.headers.get("Location")
if redirect_url:
    print("Redirect URL:", redirect_url)

    # Now, make a GET request to the redirected URL
    redirected_response = session.get(redirect_url, headers=headers)
    print("Status Code of Redirected URL:", redirected_response.status_code)
    #print("Content of Redirected URL:", redirected_response.text)
else:
    print("No redirection occurred or 'Location' header not found.")

# Print the status code and headers of the initial response

print("Initial Response Headers:", redirected_response.headers)
