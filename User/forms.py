from cgitb import text

from django import forms
from .models import Contact_Us


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact_Us
        fields = ['subject', 'text']
        widgets = {
            'subject': forms.TextInput(attrs={
                "id": "subject",
                "class": "form-control",
                "onfocus": "this.placeholder = ''",
                "onblur": "this.placeholder = 'موضوع'",
                "placeholder": "موضوع"
            }),
            "text": forms.Textarea(attrs={
                "class": "form-control w-100",
                "id": "message",
                "cols": "30",
                "rows": "9",
                "onfocus": "this.placeholder = ''",
                "onblur": "this.placeholder = 'متن پیام'",
                "placeholder": " متن پیام"
            })
        }
