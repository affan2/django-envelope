# -*- coding: utf-8 -*-



"""
Views used to process the contact form.
"""

import logging
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _

from . import signals
from .forms import ContactForm

logger = logging.getLogger('envelope.views')


class ContactView(FormView):
    """
    Contact form view (class-based).

    Displays the contact form upon a GET request. If the current user is
    authenticated, ``sender`` and ``email`` fields are automatically
    filled with proper values.

    When the form is submitted and valid, a message is sent and
    afterwards the user is redirected to a "thank you" page (by default
    it is the page with the form).

    ``form_class``
        Which form class to use for contact message handling.
        The default (:class:`envelope.forms.ContactForm`) is often
        enough, but you can subclass it if you want, or even replace
        with a totally custom class. The only requirement is that your
        custom class has a ``save()`` method which should send the
        message somewhere. Stick to the default, or its subclasses.

    ``form_kwargs``
        Additional kwargs to be used in the creation of the form. Use
        with :class:`envelope.forms.BaseContactForm` form arguments for
        dynamic customization of the form.

    ``template_name``
        Full name of the template which will display
        the form. By default it is "envelope/contact.html".

    ``success_url``
        URL of the page with some kind of a "thank you
        for your feedback", displayed after the form is successfully
        submitted. If left unset, the view redirects to itself.
    """
    form_class = ContactForm
    form_kwargs = {}
    template_name = 'envelope/contact.html'
    success_url = None

    def get_success_url(self):
        """
        Returns the URL where the view will redirect after submission.
        """
        if self.success_url:
            return self.success_url
        else:
            return self.request.get_full_path()

    def get_initial(self):
        """
        Automatically fills form fields for authenticated users.
        """
        initial = super(ContactView, self).get_initial().copy()
        user = self.request.user
        if user.is_authenticated():
            # the user might not have a full name set in the model
            if user.get_full_name():
                sender = '%s (%s)' % (user.username, user.get_full_name())
            else:
                sender = user.username
            initial.update({
                'sender': sender,
                'email': user.email,
            })
        return initial

    def get_form_kwargs(self):
        kwargs = super(ContactView, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_valid(self, form):
        """
        Sends the message and redirects the user somewhere.
        """
        responses = signals.before_send.send(sender=self.__class__,
                                             request=self.request,
                                             form=form)
        for (receiver, response) in responses:
            if not response:
                error_message = _("Rejected by %s") % receiver.__name__
                return HttpResponseBadRequest(error_message)
        form.save()
        messages.info(self.request,
                      _("Thank you for your message."),
                      fail_silently=True)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """
        When the form has errors, display it again.
        """
        messages.error(self.request,
                       _("There was an error in the contact form."),
                       fail_silently=True)
        return self.render_to_response(self.get_context_data(form=form))


class BaseContact(CreateView):
    user = None
    company = None
    form = None
    object = None
    form_kwargs = {}
    success_url = None

    def get_initial(self):
        """
        Automatically fills form fields for authenticated users.
        """
        initial = super(BaseContact, self).get_initial().copy()
        user = self.request.user
        if user.is_authenticated():
            # the user might not have a full name set in the model
            if user.get_full_name():
                sender = '%s' % user.get_full_name()
            else:
                sender = user.username
            initial.update({
                'sender': sender,
                'email': user.email,
            })
        return initial

    def get_form_kwargs(self):
        kwargs = super(BaseContact, self).get_form_kwargs()
        del kwargs['instance']
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):
        """
        When the form has errors, display it again.
        """
        messages.error(self.request,
                       _("There was an error in the contact form."),
                       fail_silently=True)
        return self.render_to_response(self.get_context_data(form=form))

    def dispatch(self, *args, **kwargs):
        return super(BaseContact, self).dispatch(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )


# def filter_spam(sender, request, form, **kwargs):
#     """
#     Handle spam filtering.
#
#     This function is called when the ``before_send`` signal fires,
#     passing the current request and form object to the function.
#     With that information in hand, all available spam filters are called.
#
#     TODO: more spam filters
#     """
#     if issubclass(sender, ContactView):
#         from envelope.spam_filters import check_honeypot
#         return check_honeypot(request, form)
#
#
# signals.before_send.connect(filter_spam,
#                             dispatch_uid='envelope.views.filter_spam')
