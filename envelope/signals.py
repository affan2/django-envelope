# -*- coding: utf-8 -*-



"""
Signals sent by the application.
"""

from django.dispatch import Signal

before_send = Signal(providing_args=["request", "form"])
after_send = Signal(providing_args=["message", "form"])
