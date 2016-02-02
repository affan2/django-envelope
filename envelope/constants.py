from django.utils.translation import ugettext_lazy as _

STATE_TYPES = (
    (-1, _('Deleted')),
    (1, _('Replied')),
    (2, _('Pending')),
)


COMPANY_CONTACT_CHOICES = (
    ("", u''),
    ("First choice", _('First choice')),
    ("Second choice", _('Second choice')),
    ("Third choice", _('Third choice')),
)

PRODUCT_CONTACT_CHOICES = (
    ("", u''),
    ("First choice", _('First choice')),
    ("Second choice", _('Second choice')),
    ("Third choice", _('Third choice')),
)

SOLUTIONS_CONTACT_CHOICES = (
    ("", u''),
    ("First choice", _('First choice')),
    ("Second choice", _('Second choice')),
    ("Third choice", _('Third choice')),
)