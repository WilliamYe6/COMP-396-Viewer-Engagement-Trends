import os
import argparse
import csv
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv

#load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')

#initialize youtube object
youtube = build('youtube', 'v3', developerKey=API_KEY)
     
# Function to get video statistics
def get_video_statistics(video_id, writer):
  
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    video_response = request.execute()
    if "items"  not in video_response or len(video_response["items"]) < 1:
        return

    title = video_response.get('items', [{}])[0].get('snippet', {}).get('title', 'N/A')
    #title = video_response['items'][0]['snippet']['title']
    #gets channel name
    title = video_response.get('items', [{}])[0].get('snippet', {}).get('title', 'N/A')
    channel = video_response.get('items', [{}])[0].get('snippet', {}).get('channelTitle', 'N/A')
    view_count = video_response.get('items', [{}])[0].get('statistics', {}).get('viewCount', 'N/A')
    like_count = video_response.get('items', [{}])[0].get('statistics', {}).get('likeCount', 'N/A')
    comment_count = video_response.get('items', [{}])[0].get('statistics', {}).get('commentCount', 'N/A')
 
    published_date = video_response['items'][0]['snippet']['publishedAt']
    #temp_duration = video_response['items'][0]['contentDetails']['duration']
    duration = video_response.get('items', [{}])[0].get('contentDetails', {}).get('duration', 'N/A')
    #convert duration
   
    if (duration != 'N/A'):
        duration = duration_conversion(duration)
    
    

    #dislikes count
    dislike_url = 'https://returnyoutubedislikeapi.com/votes?videoId='+video_id
    dislike_response = requests.get(dislike_url)
    dislike_count = '-1'
    if dislike_response.status_code == 200:
        dislike_json = dislike_response.json()
        dislike_count = dislike_json['dislikes']

    #used to get channel id
    channel_id = video_response['items'][0]['snippet']['channelId']
    
    #channel response based on id
    channel_response = youtube.channels().list(
        part='statistics',
        id=channel_id
    ).execute()

    #gets channel subscribers
    channel_subscribers = channel_response['items'][0]['statistics']['subscriberCount']

    #populate row in csv
    writer.writerow({
        'Video ID': video_id,
        'Title': title,
        'Channel': channel,
        'Channel Subscribers': channel_subscribers,
        'View Count': view_count, 
        'Likes': like_count,
        'Dislikes': dislike_count,
        'Comment Count': comment_count, 
        'Published Date': published_date, 
        'Duration': duration
    })
# Function to fetch all playlist videos (including paginated results)
def get_all_playlist_videos(playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_ids.append(item["snippet"]["resourceId"]["videoId"])

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return video_ids

def duration_conversion(duration):
    import re
    match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration)

    if match == None:
        return 'N/A'
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return str(hours * 3600 + minutes * 60 + seconds)
    
        

# Example usage
def main():

    #initialising script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=str, help="csv file to write in")
    parser.add_argument("list_of_video_ids", type=str, help="list of youtube playlist ids to query")

    args = parser.parse_args()
    
    #open input list file
    with open(args.list_of_video_ids, mode='r') as input_text:
        playlist_id_list = input_text.read().split(",")
    
    #creating csvfile to hold youtube metadata
    with open(args.csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Video ID', 'Title', 'Channel', 'Channel Subscribers', 'View Count', 'Likes', 'Dislikes','Comment Count', 'Published Date', 'Duration']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for playlist_id in playlist_id_list:
            video_ids = get_all_playlist_videos(playlist_id)
            for video_id in video_ids:
                get_video_statistics(video_id, writer)
                


if __name__ == "__main__":
    main()