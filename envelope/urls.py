# -*- coding: utf-8 -*-

try:
    # Django 1.6+
    from django.conf.urls import patterns, url
except ImportError:  # pragma: no cover
    # Django 1.4 and 1.5
    from django.conf.urls.defaults import patterns, url

from envelope.views import ContactView

urlpatterns = patterns('',
    url(r'^$', ContactView.as_view(), name='envelope-contact'),
    # url(r'^(?P<company_slug>[a-zA-Z0-9\-]+)/$', CompanyContactList.as_view(), name='company_contact'),
    # url(r'^(?P<company_slug>[a-zA-Z0-9\-]+)/company/contact/$', CompanyContactAdd.as_view(), name='company_contact'),
    # url(r'^(?P<product_slug>[a-zA-Z0-9\-]+)/product/contact/$', ProductContactAdd.as_view(), name='product_contact'),
    # # url(r'^(?P<solution_slug>[a-zA-Z0-9\-]+)/solution/contact/$', SolutionContactAdd.as_view(), name='solution_contact'),
    # url(r'^(?P<company_slug>[a-zA-Z0-9\-]+)/(?P<email_type>[a-zA-Z0-9\-]+)/$', CompanyContactList.as_view(), name='company_contact'),
    # url(r'^detail/(?P<company_slug>[a-zA-Z0-9\-]+)-(?P<email_id>[a-zA-Z0-9\-]+)$', CompanyContactDetail.as_view(), name='company_contact_detail'),


    # url(r'^(?P<solutions_slug>[a-zA-Z0-9\-]+)/add/$', SolutionContactAdd.as_view(), name='solution_contact'),
)