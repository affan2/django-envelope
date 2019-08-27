from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .constants import STATE_TYPES

from django.contrib.auth import get_user_model


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
        get_user_model(),
        related_name="%(app_label)s_%(class)s_created_by_",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    updated = models.DateTimeField(
        verbose_name=_('Update date'),
        auto_now=True,
        editable=False,
    )
    updated_by = models.ForeignKey(
        get_user_model(),
        related_name="%(app_label)s_%(class)s_updated_by_",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    user_email = models.EmailField(verbose_name=_('Email'))

    class Meta:
        abstract = True
