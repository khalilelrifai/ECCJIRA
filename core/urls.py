# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path  # add this
from django.views.static import serve

from core.settings import BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # Leave `Home.Urls` as last the last line

    path("reports/", include("apps.reports.urls")),
    path("trips/", include("apps.trips.urls")),
    path("bulletins/", include("apps.bulletins.urls")),
    path("assignment/", include("apps.assignment.urls")),
    path("", include("apps.home.urls")),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'apps/static'),
        }
    ),
]