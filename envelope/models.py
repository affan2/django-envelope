from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .constants import STATE_TYPES
from companies.models import Company
from phonenumber_field.modelfields import PhoneNumberField
from urlparse import urlparse


class BaseContact(models.Model):

    state = models.SmallIntegerField(
        verbose_name=_('State'),
        choices=STATE_TYPES,
        default=2,
    )
    user_email = models.EmailField()
    created = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True,
        editable=False,
    )
    created_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_created_by_",
        null=True,
        blank=True,
    )
    updated = models.DateTimeField(
        verbose_name=_('Update date'),
        auto_now=True,
        editable=False,
    )
    updated_by = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_updated_by_",
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        verbose_name=_('Company')
    )
    contact_company = models.TextField(
        verbose_name=_('Contact Company')
    )
    contact_job_title = models.TextField(
        verbose_name=_('Job Title')
    )
    contact_phone = PhoneNumberField(
        verbose_name=_('Phone'),
        help_text='The number should be in international format - +int area number.'
    )
    message_box = models.TextField(
        verbose_name=_('Message')
    )
    subject = models.TextField(
        verbose_name=_('Subject')
    )

    class Meta:
        abstract = True



class CompanyContact(BaseContact):

    def save(self, *args, **kwargs):
        super(CompanyContact, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s from %s' % (self.subject, self.user_email)

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def full_url(self):
        request = None
        domain = urlparse(get_current_site(request).domain)
        if domain.scheme:
            return '%s%s' % (get_current_site(request).domain, self.get_absolute_url())
        else:
            return '%s://%s%s' % (settings.DEFAULT_HTTP_PROTOCOL, get_current_site(request).domain, self.get_absolute_url())

    def get_absolute_url(self):
        url_name = 'company_contact_detail'
        kwargs = {
            'id': self.id,
            'contact_type': 'company'
        }
        return reverse(url_name, kwargs=kwargs)


class ProductContact(BaseContact):

    def save(self, *args, **kwargs):
        super(ProductContact, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s from %s' % (self.subject, self.user_email)

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def full_url(self):
        request = None
        domain = urlparse(get_current_site(request).domain)
        if domain.scheme:
            return '%s%s' % (get_current_site(request).domain, self.get_absolute_url())
        else:
            return '%s://%s%s' % (settings.DEFAULT_HTTP_PROTOCOL, get_current_site(request).domain, self.get_absolute_url())

    def get_absolute_url(self):
        url_name = 'product_contact_detail'
        kwargs = {
            'id': self.id,
            'contact_type': 'product'
        }
        return reverse(url_name, kwargs=kwargs)

class SolutionContact(BaseContact):

    def save(self, *args, **kwargs):
        super(SolutionContact, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s from %s' % (self.subject, self.user_email)

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def full_url(self):
        request = None
        domain = urlparse(get_current_site(request).domain)
        if domain.scheme:
            return '%s%s' % (get_current_site(request).domain, self.get_absolute_url())
        else:
            return '%s://%s%s' % (settings.DEFAULT_HTTP_PROTOCOL, get_current_site(request).domain, self.get_absolute_url())

    def get_absolute_url(self):
        url_name = 'product_contact_detail'
        kwargs = {
            'id': self.id,
            'contact_type': 'solution'
        }
        return reverse(url_name, kwargs=kwargs)