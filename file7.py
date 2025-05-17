# import requests
# import re

# API_KEY = 'your api key'
# CHANNEL_ID = 'channele id'  # Replace with your channel's ID

# def get_uploads_playlist_id(channel_id):
#     url = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={API_KEY}'
#     response = requests.get(url).json()
#     if "items" not in response or len(response['items']) == 0:
#         raise Exception(f"Channel not found or API error: {response}")
#     return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# def get_recent_videos(playlist_id, max_results=10):
#     url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}'
#     response = requests.get(url).json()
#     if "items" not in response:
#         raise Exception(f"Playlist items not found or API error: {response}")
#     return response['items']

# def extract_hashtags(description):
#     return re.findall(r"#\w+", description)

# def main():
#     uploads_playlist_id = get_uploads_playlist_id(CHANNEL_ID)
#     videos = get_recent_videos(uploads_playlist_id, max_results=10)

#     for video in videos:
#         snippet = video['snippet']
#         title = snippet['title']
#         description = snippet.get('description', '')
#         video_id = snippet['resourceId']['videoId']
#         video_url = f"https://www.youtube.com/watch?v={video_id}"
#         hashtags = extract_hashtags(description)
        
#         print(f"Title: {title}")
#         print(f"URL: {video_url}")
#         print(f"Hashtags: {hashtags}")
#         print("-" * 40)

# if __name__ == "__main__":
#     main()


import requests
import re
from datetime import datetime

API_KEY = 'your api key'
CHANNEL_ID = 'channele id'  # Replace with your channel's ID

def get_channel_info(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}'
    response = requests.get(url).json()
    if "items" not in response or len(response['items']) == 0:
        raise Exception(f"Channel not found or API error: {response}")
    item = response['items'][0]
    snippet = item['snippet']
    statistics = item['statistics']
    return {
        "channelTitle": snippet.get('title', ''),
        "verified": item.get('brandingSettings', {}).get('channel', {}).get('keywords', '').find('YouTube Verified') != -1,
        "subscriberCount": statistics.get('subscriberCount', 'N/A')
    }

def get_uploads_playlist_id(channel_id):
    url = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={API_KEY}'
    response = requests.get(url).json()
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_recent_videos(playlist_id, max_results=10):
    url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}'
    response = requests.get(url).json()
    return response['items']

def get_video_details(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={video_id}&key={API_KEY}'
    response = requests.get(url).json()
    if "items" not in response or len(response['items']) == 0:
        return None
    item = response['items'][0]
    snippet = item['snippet']
    stats = item['statistics']
    content = item['contentDetails']

    return {
        "title": snippet['title'],
        "description": snippet.get('description', ''),
        "publishedAt": snippet.get('publishedAt'),
        "duration": parse_iso_duration(content.get('duration', '')),
        "viewCount": stats.get('viewCount', 'N/A'),
        "likeCount": stats.get('likeCount', 'N/A'),
        "commentCount": stats.get('commentCount', 'N/A'),
        "hashtags": extract_hashtags(snippet.get('description', '')),
    }

def extract_hashtags(text):
    return re.findall(r"#\w+", text)

def parse_iso_duration(duration):
    # Converts ISO 8601 duration (e.g., PT5M33S) into HH:MM:SS format
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def format_date(iso_date):
    dt = datetime.strptime(iso_date, '%Y-%m-%dT%H:%M:%SZ')
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def main():
    channel_info = get_channel_info(CHANNEL_ID)
    uploads_playlist_id = get_uploads_playlist_id(CHANNEL_ID)
    videos = get_recent_videos(uploads_playlist_id, max_results=10)

    print(f"Channel: {channel_info['channelTitle']}")
    print(f"Verified: {'Yes' if channel_info['verified'] else 'No'}")
    print(f"Subscribers: {channel_info['subscriberCount']}")
    print("=" * 60)

    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        details = get_video_details(video_id)
        if not details:
            continue

        print(f"Title: {details['title']}")
        print(f"Published At: {format_date(details['publishedAt'])}")
        print(f"Duration: {details['duration']}")
        print(f"Views: {details['viewCount']}")
        print(f"Likes: {details['likeCount']}")
        print(f"Comments: {details['commentCount']}")
        print(f"Hashtags: {details['hashtags']}")
        print(f"Description: {details['description'][:100]}...")  # Truncated
        print(f"URL: https://www.youtube.com/watch?v={video_id}")
        print("-" * 60)

if __name__ == "__main__":
    main()
