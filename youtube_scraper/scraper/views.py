from django.shortcuts import render
from .utils import get_youtube_data
from googleapiclient.errors import HttpError

def welcome(request):
    return render(request, 'welcome.html')

def Result(request):
    return render(request, 'result.html')

def youtube_analysis(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        try:
            title, comments, title_sentiment, comments_sentiment = get_youtube_data(video_url)
        except ValueError as e:
            return render(request, 'index.html', {
                'error': str(e),
            })
        except HttpError as e:
            return render(request, 'index.html', {
                'error': "An error occurred with the YouTube API: " + str(e),
            })

        return render(request, 'result.html', {
            'title': title,
            'comments': zip(comments, comments_sentiment),
        })
    return render(request, 'index.html')
