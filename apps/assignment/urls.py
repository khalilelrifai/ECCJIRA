from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name='assignment'


urlpatterns = [
    path('', login_required(upload_video), name='main'),
    path('upload/',login_required(upload_video), name='upload_video'),
    path('videoslist/', login_required(VideoListView.as_view()), name='video_list'),
    path('mylist/', login_required(OwnerVideoListView.as_view()), name='my_list'),
    path('list/detail/<int:pk>/', login_required(VideoDetailView.as_view()), name='video_detail'),
]
