import pandas as pd
import isodate
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime

def fetch_videos_data(youtube, channel_id):
    videos_data = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=50,
            type="video",
            pageToken=next_page_token
        )
        response = request.execute()

        video_ids = [item['id']['videoId'] for item in response['items']]
        videos_request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=','.join(video_ids)
        )
        videos_response = videos_request.execute()

        for video in videos_response['items']:
            video_data = {
                'Video ID': video['id'],
                'Title': video['snippet']['title'],
                'Description': video['snippet']['description'],
                'Published date': video['snippet']['publishedAt'],
                'View count': video['statistics'].get('viewCount', 0),
                'Like count': video['statistics'].get('likeCount', 0),
                'Comment count': video['statistics'].get('commentCount', 0),
                'Duration': isodate.parse_duration(video['contentDetails']['duration']).total_seconds(),
                'Thumbnail URL': video['snippet']['thumbnails']['default']['url']
            }
            videos_data.append(video_data)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos_data


def fetch_comments_data(youtube, videos_data):
    comments_data = []
    total_comments = 0

    for video in videos_data:
        if total_comments >= 100:
            break

        try:
            comments_request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video['Video ID'],
                maxResults=100,
                order="time"  # sort by date
            )
            while comments_request and total_comments < 100:
                comments_response = comments_request.execute()

                for item in comments_response['items']:
                    if total_comments >= 100:
                        break

                    comment = item['snippet']['topLevelComment']['snippet']
                    comment_data = {
                        'Video ID': video['Video ID'],
                        'Comment ID': item['id'],
                        'Comment text': comment['textDisplay'],
                        'Author name': comment['authorDisplayName'],
                        'Published date': comment['publishedAt'],
                        'Like count': comment['likeCount'],
                        'Reply to': ''
                    }
                    comments_data.append(comment_data)
                    total_comments += 1

                    # Process replies if available and within the limit
                    if 'replies' in item:
                        for reply in item['replies']['comments']:
                            if total_comments >= 100:
                                break
                            reply_data = {
                                'Video ID': video['Video ID'],
                                'Comment ID': reply['id'],
                                'Comment text': reply['snippet']['textDisplay'],
                                'Author name': reply['snippet']['authorDisplayName'],
                                'Published date': reply['snippet']['publishedAt'],
                                'Like count': reply['snippet']['likeCount'],
                                'Reply to': item['id']
                            }
                            comments_data.append(reply_data)
                            total_comments += 1

                # Handle pagination
                comments_request = youtube.commentThreads().list_next(comments_request, comments_response)

        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred while fetching comments for video {video['Video ID']}: {e}")
            continue
    comments_data = sorted(
        comments_data,
        key=lambda x: datetime.strptime(x['Published date'], '%Y-%m-%dT%H:%M:%SZ'),
        reverse=True
    )
    return comments_data


def write_to_excel(videos_data, comments_data):
    with pd.ExcelWriter('youtube_channel_data.xlsx') as writer:
        videos_df = pd.DataFrame(videos_data)
        videos_df.to_excel(writer, sheet_name='Video Data', index=False)
        comments_df = pd.DataFrame(comments_data)
        comments_df.to_excel(writer, sheet_name='Comments Data', index=False)

    print("Data has been written to youtube_channel_data.xlsx")