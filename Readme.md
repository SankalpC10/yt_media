# YouTube Channel Data Scraper

This Python application extracts data from a specified YouTube channel, including video metadata and comments, and saves the results to an Excel file. It leverages the YouTube Data API v3 and uses OAuth 2.0 for secure access.

## Features

- Fetches metadata for videos from a specified YouTube channel.
- Retrieves top comments and their replies for each video.
- Saves all collected data into an Excel file with separate sheets for video data and comments.

## Prerequisites

1. **Google Developer Account**: You need to create a project in the [Google Developers Console](https://console.developers.google.com/) to enable the YouTube Data API v3 and obtain credentials.
2. **Python Libraries**: Install the required packages via `pip install -r requirements.txt`.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SankalpC10/yt_media.git
   cd yt_media
   ```
   
2. **Install Required Libraries**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Authentication**
    By API KEY - Environment Variables:
    Create a .env file and add your YouTube Data API key:
    ```bash
    YOUTUBE_API_KEY=your_youtube_api_key_here
   ```
    By Oauth - Google API Credentials:
    Download your client_secret_yt_media.json file from the Google Developer Console and place it in the project directory.

4. **Usage** :
 Run the Application:
    ```bash
    python main.py
    ```

    Provide Channel URL:
    Enter the URL of the YouTube channel (e.g.,https://www.youtube.com/@GoQuest_Media) when prompted.

    Data Output:
    The script will generate an youtube_channel_data.xlsx file in the project directory with video and comments data.

5. **Configuration** :
The script supports two authentication methods:
- OAuth Flow (recommended for more secure access): It will prompt you to authenticate via Google when running.
- API Key Flow (faster, but requires API key setup): Uncomment the relevant lines in main.py and comment out the OAuth sections.

6. **Files** :
- main.py: The main script that handles authentication and data extraction.
- utils.py: Contains helper functions to fetch video metadata, comments, and save data to Excel.
- requirements.txt: List of required Python packages.

7. **Error Handling** : 
The script includes error handling for common API issues, such as invalid credentials and quota limits. If an error occurs, the script will display an error message in the console and proceed to the next item.