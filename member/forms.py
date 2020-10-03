from django import forms
from django.contrib.auth.models import User 

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Repeat password', 
        widget=forms.PasswordInput
    )

    class Meta:
        model=User 
        fields = ('username', 'email')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already taken")
        return email

    def clean_password2(self):
        cd =self.cleaned_data 
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\' t match')
        return cd['password2']
