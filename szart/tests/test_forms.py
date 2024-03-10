from django.test import TestCase
from szartapp.forms import MessageForm
from django import forms

class MessageFormTest(TestCase):
    def test_form_fields(self):
        # Properties of the form fields
        message_form = MessageForm({
            'nadawca': 'jakis_user',
            'email': 'any@gmail.com',
            'temat': 'subject',
            'tresc' : 'user_message'
        })

        # print(message_form.fields) - spr typu fielda
        self.assertTrue(isinstance(message_form.fields['nadawca'], forms.CharField))
        self.assertTrue(isinstance(message_form.fields['email'], forms.EmailField))
        self.assertTrue(isinstance(message_form.fields['temat'], forms.CharField))
        self.assertTrue(isinstance(message_form.fields['tresc'], forms.CharField))


        # Test invalid inputs
        message_form = MessageForm({
            'nadawca': 'jakis_user',
            'email': '',
        })
        self.assertFalse(message_form.is_valid())
        self.assertNotIn('email', message_form.cleaned_data)

        # Test valid inputs
        message_form = MessageForm({
            'nadawca': 'jakis_user',
            'email': 'any@gmail.com',
            'temat': 'subject',
            'tresc' : 'user_message'
        })
        self.assertTrue(message_form.is_valid())
        cleaned_data = message_form.cleaned_data
        self.assertEqual(cleaned_data['nadawca'], 'jakis_user')
        self.assertEqual(cleaned_data['email'], 'any@gmail.com')
        self.assertEqual(cleaned_data['temat'], 'subject')
        self.assertEqual(cleaned_data['tresc'], 'user_message')