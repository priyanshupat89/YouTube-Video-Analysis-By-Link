# import re
# import googleapiclient.discovery
# from googleapiclient.errors import HttpError
# from textblob import TextBlob

# # Define the API key and API service
# API_KEY = 'AIzaSyB-jURCrabxMf2_k8VH1zAydTlD4_M2YCE'
# API_SERVICE_NAME = 'youtube'
# API_VERSION = 'v3'

# def extract_video_id(url):
#     """
#     Extracts the video ID from a YouTube URL, handling different formats.
#     Returns the video ID if valid, otherwise raises a ValueError.
#     """
#     regex = (r'(?:https?://)?(?:www\.)?'
#              '(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)|.*[?&]v=)|youtu\.be/)'
#              '([^"&?/ ]{11})')

#     match = re.match(regex, url)
#     if match:
#         return match.group(1)
#     else:
#         raise ValueError("Invalid YouTube URL")

# def get_youtube_data(video_url):
#     # Extract the video ID from the URL
#     try:
#         video_id = extract_video_id(video_url)
#     except ValueError as e:
#         raise ValueError("Invalid YouTube URL")

#     # Create a YouTube API client
#     youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

#     # Get video title
#     video_response = youtube.videos().list(
#         part='snippet',
#         id=video_id
#     ).execute()

#     if not video_response['items']:
#         raise ValueError("No video found for the given URL")

#     title = video_response['items'][0]['snippet']['title']

#     # Get comments
#     comments = []
#     try:
#         comment_response = youtube.commentThreads().list(
#             part='snippet',
#             videoId=video_id,
#             maxResults=10
#         ).execute()

#         for item in comment_response.get('items', []):
#             comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
#             comments.append(comment)

#     except HttpError as e:
#         # Handle 403 error when comments are disabled
#         if e.resp.status == 403 and 'commentsDisabled' in str(e):
#             comments = ["Comments are disabled for this video."]
#         else:
#             raise e

#     # Analyze sentiment
#     title_sentiment = analyze_sentiment(title)
#     comments_sentiment = [analyze_sentiment(comment) for comment in comments]

#     return title, comments, title_sentiment, comments_sentiment

# def analyze_sentiment(text):
#     analysis = TextBlob(text)
#     if analysis.sentiment.polarity > 0:
#         return 'Positive'
#     elif analysis.sentiment.polarity == 0:
#         return 'Neutral'
#     else:
#         return 'Negative'
import re
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Define the API key and API service
API_KEY = 'AIzaSyB-jURCrabxMf2_k8VH1zAydTlD4_M2YCE'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Initialize the VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL, handling different formats.
    Returns the video ID if valid, otherwise raises a ValueError.
    """
    regex = (r'(?:https?://)?(?:www\.)?'
             '(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)|.*[?&]v=)|youtu\.be/)'
             '([^"&?/ ]{11})')

    match = re.match(regex, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_youtube_data(video_url):
    # Extract the video ID from the URL
    try:
        video_id = extract_video_id(video_url)
    except ValueError as e:
        raise ValueError("Invalid YouTube URL")

    # Create a YouTube API client
    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    # Get video title
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    if not video_response['items']:
        raise ValueError("No video found for the given URL")

    title = video_response['items'][0]['snippet']['title']

    # Get comments
    comments = []
    try:
        comment_response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=10
        ).execute()

        for item in comment_response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

    except HttpError as e:
        # Handle 403 error when comments are disabled
        if e.resp.status == 403 and 'commentsDisabled' in str(e):
            comments = ["Comments are disabled for this video."]
        else:
            raise e

    # Analyze sentiment using VADER
    title_sentiment = analyze_sentiment(title)
    comments_sentiment = [analyze_sentiment(comment) for comment in comments]

    return title, comments, title_sentiment, comments_sentiment

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using VADER.
    Returns 'Positive', 'Negative', or 'Neutral' based on the compound score.
    """
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    if compound_score > 0:
        return 'Positive'
    elif compound_score == 0:
        return 'Neutral'
    else:
        return 'Negative'
