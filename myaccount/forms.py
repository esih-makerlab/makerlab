from django import forms
from django.contrib.auth.models import User


class SignUpUser(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*********'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ex: Jesuibogos'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'EX: james_ok.gmail.ok'}),
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data

