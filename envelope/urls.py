# -*- coding: utf-8 -*-

from django.urls import re_path, include

from .views import ContactView


urlpatterns = [
    re_path(r'^contact/', include('django-envelope.envelope.urls')),
    re_path(r'^$', ContactView.as_view(), name='envelope-contact'),
]
