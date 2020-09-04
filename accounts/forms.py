from django import forms
from django.contrib.auth.models import User


class SignUpUser(forms.ModelForm):
    password = forms.EmailField(widget=forms.EmailInput(attrs={'class': '', 'placeholder': '********'}))
    

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ex: iambest'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Ex: Jae@gmail.com'}),
        }

     def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email