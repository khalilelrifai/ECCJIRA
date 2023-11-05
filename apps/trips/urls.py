from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

app_name = 'trips'

urlpatterns = [
    path('', login_required(TemplateView.as_view(
        template_name='trips/main.html')), name='main'),
    path('detail/<int:pk>/', TripDetailView.as_view(), name='trip_detail'),
    path('request/<int:pk>/', TripRequest.as_view(), name='trip_request'),
    path('create/', CreateTripView.as_view(), name='create'),
    path('list/', TripListView.as_view(), name='list'),


]
