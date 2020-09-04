from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm



class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'EX: BogoslaWow'


        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = '*********'

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

