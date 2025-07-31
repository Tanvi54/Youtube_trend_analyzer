import pandas as pd
from googleapiclient.discovery import build

API_KEY = "AIzaSyD7vADLpwAlv_DU1ey_Bz6jfZ2O2BMjqiw"
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)

def get_categories(region="IN"):
    """Fetches YouTube video categories for a region and returns a dict {id: name}."""
    request = YOUTUBE.videoCategories().list(
        part="snippet",
        regionCode=region
    )
    response = request.execute()
    categories = {item['id']: item['snippet']['title'] for item in response['items']}
    return categories

def get_trending_videos(region="IN", total_results=100):
    """
    Fetches trending YouTube videos with stats (supports pagination) 
    and saves them to CSV.
    """
    categories = get_categories(region)

    videos = []
    next_page_token = None
    fetched = 0

    while fetched < total_results:
        max_per_call = min(50, total_results - fetched)  # API allows max 50 per call
        request = YOUTUBE.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=region,
            maxResults=max_per_call,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get('items', []):
            videos.append({
                "video_id": item['id'],
                "title": item['snippet']['title'],
                "channel": item['snippet']['channelTitle'],
                "category": categories.get(item['snippet']['categoryId'], "Unknown"),
                "publish_time": item['snippet']['publishedAt'],
                "views": int(item['statistics'].get('viewCount', 0)),
                "likes": int(item['statistics'].get('likeCount', 0)),
                "comments": int(item['statistics'].get('commentCount', 0)),
                "link": f"https://www.youtube.com/watch?v={item['id']}"
            })

        fetched += len(response.get('items', []))
        next_page_token = response.get('nextPageToken')

        if not next_page_token:  # No more pages
            break

    print(f"Fetched videos: {len(videos)}")

    if not videos:
        print("No videos fetched! Check your API key or quota.")
        return pd.DataFrame()

    df = pd.DataFrame(videos)
    df.to_csv("trending_data.csv", index=False)
    print("Data saved to trending_data.csv (overwritten).")
    return df

if __name__ == "__main__":
    get_trending_videos(total_results=100)  # Change this number to fetch more videos