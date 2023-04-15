from django import forms
from django.forms import models
from .models import List
from .models import token_manage

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ["item", "completed"]

