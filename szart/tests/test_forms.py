from django.test import TestCase
from szartapp.forms import MessageForm
from django import forms

class MessageFormTest(TestCase):
    def test_form_fields(self):
        # Properties of the form fields
        message_form = MessageForm({
            'nadawca': 'jakis_user',
            'email': 'address',
            'temat': 'subject',
            'tresc' : 'user_message'
        })

        # self.assertEqual(message_form.fields['title'].widget.input_type, 'text')
        self.assertTrue(isinstance(message_form.fields['nadawca'], forms.CharField))
        self.assertTrue(isinstance(message_form.fields['email'], forms.EmailField))
        self.assertTrue(isinstance(message_form.fields['temat'], forms.CharField))
        # self.assertTrue(isinstance(message_form.fields['tresc'], forms.TextField))


