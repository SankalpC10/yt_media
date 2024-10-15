import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from datetime import datetime, timezone
from utils import fetch_videos_data,fetch_comments_data, write_to_excel
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")


scopes = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # Todo: Comment this line when running on server
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_yt_media.json"

    # Method 1: Oauth Flow - More secure but slower
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    # Method 2:API Key Flow -- Faster but requires API key
    # youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_KEY)

    channel_url = input("Enter the YouTube channel URL (e.g., https://www.youtube.com/@channel_name): ") #example: https://www.youtube.com/@GoQuest_Media ; https://www.youtube.com/@Fireship
    channel_handle = channel_url.split('@')[-1]

    try:
        # Get channel ID from handle
        channel_response = youtube.search().list(
            part="snippet",
            type="channel",
            q=channel_handle
        ).execute()

        if not channel_response['items']:
            print(f"No channel found for handle: {channel_handle}")
            return

        channel_id = channel_response['items'][0]['snippet']['channelId']

        # Fetch video data
        videos_data = fetch_videos_data(youtube, channel_id)

        # Fetch comments data
        comments_data = fetch_comments_data(youtube, videos_data)

        # Write data to Excel
        write_to_excel(videos_data, comments_data)

    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")


if __name__ == "__main__":
    main()
