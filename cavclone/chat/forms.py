from django import forms
from .models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ["content"]

    # input = forms.CharField(
    #     widget=forms.TextInput(attrs={"class": "custom-input-class"}),
    # )
