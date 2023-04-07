from django import forms
from . import models


class CreatePersoneFrom(forms.ModelForm):
    phones = forms.CharField(widget=forms.Textarea(), help_text="separeted by new line '\\n'")

    class Meta:
        model = models.Persone
        fields = {
            'name',
            'phones'
        }


class CreateRecordFrom(forms.ModelForm):
    class Meta:
        model = models.Record
        fields = {
            'name',
            'description',
            'colors',
        }


def save_model(self, request, obj, form, change):

    obj.users = request.user
    super().save_model(request, obj, form, change)