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
   
2. Install Required Libraries:
    ```bash
    pip install -r requirements.txt
    ```
3. Environment Variables:
    Create a .env file and add your YouTube Data API key:
    ```bash
  YOUTUBE_API_KEY=your_youtube_api_key_here
   ```
    
