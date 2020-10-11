from django import forms

class SearchFrom(forms.Form):
    q = forms.CharField(label='search', max_length=50)