u"""
Unit tests for ``django-envelope`` views.
"""


from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _


class ContactViewTestCase(TestCase):
    u"""
    Unit tests for ``envelope.views.contact`` view function.
    """

    def setUp(self):
        self.url = reverse('envelope-contact')
        self.honeypot = getattr(settings, 'HONEYPOT_FIELD_NAME', 'email2')

    def testGetContactForm(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "envelope/contact.html")
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def testAuthenticatedUserPrefilled(self):
        user = User.objects.create_user('test', 'test@example.org', 'password')
        logged_in = self.client.login(username='test', password='password')
        self.assertTrue(logged_in)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "envelope/contact.html")
        self.assertContains(response, 'value="test@example.org"')

    def testPostContactFormAntispamHoneypotField(self):
        response = self.client.post(self.url, {self.honeypot: 'some value'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(self.url, {self.honeypot: ''})
        self.assertEqual(response.status_code, 200)

    def testPostContactFormSenderField(self):
        self._testContactFormField('sender', 'zbyszek')

    def testPostContactFormEmailField(self):
        self._testContactFormField('email', 'test@example.com')

    def testPostContactFormCategoryField(self):
        self._testContactFormField('category', 10)

    def testPostContactFormSubjectField(self):
        self._testContactFormField('subject', 'A subject')

    def testPostContactFormMessageField(self):
        self._testContactFormField('message', 'Hello there!')

    def _testContactFormField(self, field_name, valid_value='value',
                              expected_error=_("This field is required.")):
        u"""
        Base method for testing form fields.

        First, submit the form with an empty value for the field. Then check
        if the form has an expected error associated with the field.

        Later, the form is submitted with a valid value for the field. As Django
        test case lacks a way to check if the form *doesn't* have specific
        errors, that check is implemented here.
        """
        response = self.client.post(self.url, {
            field_name: '',
            self.honeypot: '',
        })
        self.assertEqual(response.status_code, 200)
        flash_error_message = _("There was en error in the contact form.")
        self.assertContains(response, flash_error_message)
        self.assertFormError(response, 'form', field_name, expected_error)
        # submit the form again, this time with correct field value
        response = self.client.post(self.url, {
            field_name: valid_value,
            self.honeypot: '',
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(field_name not in form.errors)

    def testPostContactFormSuccessful(self):
        response = self.client.post(self.url, {
            'sender':   'zbyszek',
            'email':    'test@example.com',
            'category': 10,
            'subject':  'A subject',
            'message':  'Hello there!',
            self.honeypot: '',
        }, follow=True)
        self.assertRedirects(response, self.url)
        self.assertEquals(len(response.redirect_chain), 1)
        flash_error_message = _("There was en error in the contact form.")
        self.assertNotContains(response, flash_error_message)
        flash_success_message = _("Thank you for your message.")
        self.assertContains(response, flash_success_message)

