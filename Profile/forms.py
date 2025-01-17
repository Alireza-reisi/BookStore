from django import forms
from Bookmanager.models import book, Category


class BookForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = book
        fields = ['title', 'english_title', 'author', 'categories', 'image', 'file', 'description', 'publisher', 'translator']
