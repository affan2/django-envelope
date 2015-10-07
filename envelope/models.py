from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .constants import STATE_TYPES


class BaseContact(models.Model):

    state = models.SmallIntegerField(
        verbose_name=_('State'),
        choices=STATE_TYPES,
        default=2,
    )
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
    user_email = models.EmailField()

    class Meta:
        abstract = True
