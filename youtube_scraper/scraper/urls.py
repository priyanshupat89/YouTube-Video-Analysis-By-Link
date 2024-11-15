from django.urls import path
from . import views
from scraper.views import *

urlpatterns = [
    path('', welcome, name='welcome'), 
    path('welcome/', welcome, name='welcome'),
    path('index/', youtube_analysis, name='index'),
    path('result/', Result, name='result'),
]
