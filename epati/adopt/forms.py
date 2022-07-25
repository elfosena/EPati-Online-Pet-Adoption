from django.forms import ModelForm
from adopt.models import Pet
from django import forms

class PetCreateForm(ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name',
            'breed',
            'sex',
            'age',
            'description',
            'image',
        ]

    