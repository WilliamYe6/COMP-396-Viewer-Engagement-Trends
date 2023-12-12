import os
import argparse
import csv
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv


def main():

    #initialising script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=str, help="csv file to write in")
    parser.add_argument("list_of_video_ids", type=str, help="list of youtube video ids to query")

    #load environment variables
    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    #initialize youtube object
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    args = parser.parse_args()

    #open input list file
    with open(args.list_of_video_ids, mode='r') as input_text:
        video_id_list = input_text.read().split(",")

    #creating csvfile to hold youtube metadata
    with open(args.csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Video ID', 'Title', 'Channel', 'Channel Subscribers', 'View Count', 'Likes', 'Dislikes', 'Comments', 'Comment Count', 'Published Date', 'Duration', 'Category']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    
        #for every video id inside video_id_list
        for video_id in video_id_list:
            request = youtube.videos().list(
                part='snippet, contentDetails, statistics',
                id = video_id
            )
            video_response = request.execute()
            title = video_response['items'][0]['snippet']['title']
            #gets channel name
            channel = video_response['items'][0]['snippet']['channelTitle']
            view_count = video_response['items'][0]['statistics']['viewCount']
            like_count = video_response['items'][0]['statistics']['likeCount']
            comment_count = video_response['items'][0]['statistics']['commentCount']
            published_date = video_response['items'][0]['snippet']['publishedAt']
            temp_duration = video_response['items'][0]['contentDetails']['duration']

            #convert durartion
            duration = duration_conversion(temp_duration)
        
            #dislikes count
            dislike_url = 'https://returnyoutubedislikeapi.com/votes?videoId='+video_id
            dislike_response = requests.get(dislike_url)
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
        
            category_id = video_response['items'][0]['snippet']['categoryId']

            #category response based on category id
            categories_response = youtube.videoCategories().list(
                part='snippet',
                id=category_id
            ).execute()

            #gets category
            category = categories_response['items'][0]['snippet']['title']

            #comments 
            comments_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=300
            ).execute()

            comments = []
            for item in comments_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            #populate row in csv
            writer.writerow({
                'Video ID': video_id,
                'Title': title,
                'Channel': channel,
                'Channel Subscribers': channel_subscribers,
                'View Count': view_count, 
                'Likes': like_count,
                'Dislikes': dislike_count,
                'Comments': comments, 
                'Comment Count': comment_count, 
                'Published Date': published_date, 
                'Duration': duration, 
                'Category': category
            })


def duration_conversion(duration):
    import re
    match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return str(hours * 3600 + minutes * 60 + seconds)


if __name__ == "__main__":
    main()