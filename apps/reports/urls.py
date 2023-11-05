


from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic.base import TemplateView

from . import views

app_name='reports'

urlpatterns = [


    path('', login_required(TemplateView.as_view(template_name='reports/main.html')), name='main'),
    path('create',views.CreateReport.as_view(),name='create'),
    path('list',views.ReportListView.as_view(),name='list'),
    path('list/detail/<int:pk>',views.ReportDetailView.as_view(),name='L-detail'),
    path('director/detail/<int:pk>',views.ReportDetailView.as_view(),name='D-detail'),
    path('list/edit/<int:pk>',views.ReportUpdateView.as_view(),name='edit'),
    path('list/delete/<int:pk>',views.ReportDeleteView.as_view(),name='delete'),
    path('director',views.DirectorView.as_view(),name='director'),
    path('approve/<int:pk>',views.approve,name='approve'),
    path('hr',views.HRView.as_view(),name='hr'),
    path('hr/detail/<int:pk>',views.ReportDetailView.as_view(),name='H-detail'),
    path('hr/profile/<int:pk>',views.ProfileView.as_view(),name='profile'),
    
    # path('search',views.ReportsSearchList.as_view(),name='search'),
]
    # # Matches any html file
    # path('reportform/', views.reportform, name='reportform'),
    # path('submitted-report/<int:page>/',login_required(views.ReportsListView.as_view()), name='submitted'),
    
    # path('submitted-report/view/<int:pk>', login_required(views.DetailView.as_view()), name='view'),
    
    # path('profile/edit/<id>', views.edit_report, name='edit_profile'),
    # path('profile/view/<int:pk>', login_required(views.DetailView.as_view()), name='view_profile'),
    # path('profile/<int:page>/', login_required(views.ReportsListView.as_view()), name='profile'),
    # path('all/', login_required(views.ReportsListView.as_view()), name='all'),
    # ]
#     path(
#     "terms.json",
#     views.listing_api,
#     name="terms-api"
# ),
#     path("faux/",AllKeywordsView.as_view(template_name="home/test.html")),

