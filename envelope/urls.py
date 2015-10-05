# -*- coding: utf-8 -*-

try:
    # Django 1.6+
    from django.conf.urls import patterns, url
except ImportError:  # pragma: no cover
    # Django 1.4 and 1.5
    from django.conf.urls.defaults import patterns, url

from envelope.views import ContactView, CompanyContactAdd


urlpatterns = patterns('',
    url(r'^$', ContactView.as_view(), name='envelope-contact'),
    url(r'^(?P<company_slug>[a-zA-Z0-9\-]+)/add/$', CompanyContactAdd.as_view(), name='company_contact'),
    # url(r'^(?P<product_slug>[a-zA-Z0-9\-]+)/add/$', ProductContactAdd.as_view(), name='product_contact'),
    # url(r'^(?P<solutions_slug>[a-zA-Z0-9\-]+)/add/$', SolutionContactAdd.as_view(), name='solution_contact'),
)