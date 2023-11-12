


from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic.base import TemplateView

from . import views

app_name='task'

urlpatterns = [


    path('main', views.DashboardView.as_view(), name='main'),
    path('create',views.CreateTask.as_view(),name='create'),
    path('list',views.TaskListView.as_view(),name='list'),
    path('get_employees/', views.get_filtered_employees, name='get_employees'),
    path('list/detail/<int:pk>',views.TaskDetailView.as_view(),name='L-detail'),
    path('list/edit/<int:pk>',views.TaskUpdateView.as_view(),name='edit'),
    path('list/delete/<int:pk>',views.TaskDeleteView.as_view(),name='delete'),
]
    