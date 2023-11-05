
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic.base import TemplateView

from .views import *

app_name='bulletins'



urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='bulletins/create.html')), name='main'),
    path('list/', BulletinListView.as_view(), name='list'),
    path('detail/<int:bulletin_id>/', BulletinDetailView.as_view(), name='detail'),
    path('create/', CreateBulletinView.as_view(), name='create'),

]


