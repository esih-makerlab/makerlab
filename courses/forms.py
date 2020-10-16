from django import forms

class SearchFrom(forms.Form):
    q = forms.CharField(label='search', max_length=50)
    
    def clean_title(self):
        q = self.cleaned_data.get('q')

        
        
