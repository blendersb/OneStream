import requests

# URL and headers for the HLS playlist request
url = "https://b-hls-21.doppiocdn.live/hls/170894790/170894790.m3u8"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://stripchat.global/",
    "Origin": "https://stripchat.global",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Priority": "u=4",
    "TE": "trailers"
}

# Function to fetch the HLS playlist
def fetch_playlist(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch the playlist: {response.status_code}")
        return None

# Function to modify the playlist URLs
def modify_playlist(content, new_base_url):
    lines = content.splitlines()
    modified_lines = []

    for line in lines:
        # Check if the line is a media segment (starts with "http")
        if line.startswith("http"):
            # Modify the URL to use the new base URL
            segment_name = line.split('/')[-1]  # Extract segment file name
            modified_line = f"{new_base_url}/{segment_name}"
            modified_lines.append(modified_line)
        else:
            # Keep other lines (metadata) the same
            modified_lines.append(line)

    return "\n".join(modified_lines)

# Main logic
def main():
    # Fetch the playlist content
    playlist_content = fetch_playlist(url, headers)
    if playlist_content is None:
        return

    # Define the new base URL (e.g., a different server)
    new_base_url = "https://b-hls-21.doppiocdn.live/hls/176906595/176906595.m3u8"

    # Modify the playlist content with the new base URL
    modified_playlist = modify_playlist(playlist_content, new_base_url)

    # Write the modified playlist to an .m3u file
    with open("updated_playlist.m3u", "w") as file:
        file.write(modified_playlist)

    print("Playlist written to 'updated_playlist.m3u'.")

# Run the main function
if __name__ == "__main__":
    main()
