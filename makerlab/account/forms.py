from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple    
from django.contrib.auth.models import Group,Permission
import re

def notValideEmail(email):
    if email != None:
        if len(email) > 6:
            if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
                return 1
    return 0

class AddUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.help_text = None
    
    password1 = forms.CharField(
        label=_('Mot de passe'), widget=forms.PasswordInput,help_text=_('must be 8 length min')
    )
    password2 = forms.CharField(
        label=_('Confirmez le mot de passe'), widget=forms.PasswordInput,help_text=_('must be same as password')
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean(self):
          
        # extract the username and text field from the data 
        first_name = self.cleaned_data.get('first_name') 
        last_name = self.cleaned_data.get('last_name')
        email =  self.cleaned_data.get('email')
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
  
        # conditions to be met for the username length 
        if password1 and password2 and password1 != password2:
            self._errors['password1'] = self.error_class([ 
                _('Passwords do not match')])
        if len(first_name) < 3: 
            self._errors['first_name'] = self.error_class([ 
                _('Minimum 3 characters required')])
        if len(password1) < 8: 
            self._errors['password1'] = self.error_class([ 
                _('Minimum 8 characters required')])
        if len(last_name) < 3: 
            self._errors['last_name'] = self.error_class([ 
                _('Minimum 3 characters required')])  
        if notValideEmail(email): 
            self._errors['email'] = self.error_class([ 
                _('Email incorrect')]) 
  
        # return any errors if found 
        return super(AddUserForm, self).clean()

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ChangePasswordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.help_text = None
    
    old_password = forms.CharField(
        label=_('Ancien mot de passe'), widget=forms.PasswordInput,help_text=_('your old password')
    )
    password1 = forms.CharField(
        label=_('Nouveau mot de passe'), widget=forms.PasswordInput,help_text=_('must be 8 length min')
    )
    password2 = forms.CharField(
        label=_('Confirmez le  mot de passe'), widget=forms.PasswordInput,help_text=_('must be same as password')
    )

    class Meta:
        model = User
        fields = []

    def clean(self):
        
        old_password =  self.cleaned_data.get('old_password')
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
  
        # conditions to be met for the username length 
        if password1 and password2 and password1 != password2:
            self._errors['password1'] = self.error_class([ 
                _('Passwords do not match')])
        if len(password1) < 8: 
            self._errors['password'] = self.error_class([ 
                _('Minimum 8 characters required')])
        if self.instance.check_password(old_password) == False: 
            self._errors['old_password'] = self.error_class([ 
                _('Password incorrect')])
  
        # return any errors if found 
        return super(ChangePasswordForm, self).clean()

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ResetPasswordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.help_text = None
    
    password1 = forms.CharField(
        label=_('Nouveau mot de passe'), widget=forms.PasswordInput,help_text=_('must be 8 length min')
    )
    password2 = forms.CharField(
        label=_('Confirmez le mot de passe'), widget=forms.PasswordInput,help_text=_('must be same as password')
    )

    class Meta:
        model = User
        fields = []

    def clean(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
  
        # conditions to be met for the username length 
        if password1 and password2 and password1 != password2:
            self._errors['password1'] = self.error_class([ 
                _('Passwords do not match')])
        if len(password1) < 8: 
            self._errors['password'] = self.error_class([ 
                _('Minimum 8 characters required')])
  
        # return any errors if found 
        return super(ResetPasswordForm, self).clean()

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.help_text = None
    
    email = forms.EmailField(
        label=_('Email'), widget=forms.EmailInput,help_text=_('Votre email Ex:john@winterfell.got')
    )
    password = forms.CharField(
        label=_('Mot de passe'), widget=forms.PasswordInput,help_text=_('Votre mot de passe')
    )

    def clean(self):

        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if (notValideEmail(email)):
            self._errors['email'] = self.error_class([ 
                _('Email incorrect')])
        else:

            try:
                user=User.objects.get(email=email)
            except:
                user=None

            if (not user):
                self._errors['email'] = self.error_class([ 
                    _('Email not registered')])
            elif (not user.is_active):
                self._errors['email'] = self.error_class([ 
                    _('Account unactive')])
            elif (not user.check_password(password)):
                self._errors['password'] = self.error_class([ 
                    _('Password incorrect')])

        return super(LoginForm, self).clean()

class UpdateUserAdminForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """

    class Meta:
        model = User
        exclude = ['password']
    
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), 
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('groups', False)
    )

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(), 
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('permissions', False)
    )

    def clean_password(self):
        # Password can't be changed in the admin
        return self.initial["password"]

class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.help_text = None

    class Meta:
        model = User
        fields = ('email', 'photo' ,'first_name', 'last_name','password', 'phone','country')

    photo = forms.ImageField(
        label=_('Changer votre photo'),required=False,widget=forms.FileInput(attrs={'class':'d-none'})
    )

    password = forms.CharField(
        label=_('Mot de passe'), widget=forms.PasswordInput,help_text=_('Please enter your password to save')
    )

    def clean(self):
        
        first_name = self.cleaned_data.get('first_name') 
        last_name = self.cleaned_data.get('last_name')
        phone = self.cleaned_data.get('phone')
        country = self.cleaned_data.get('country')
        email =  self.cleaned_data.get('email')
        password =  self.cleaned_data.get('password')

        # conditions to be met for the username length 
        if len(first_name) < 3: 
            self._errors['first_name'] = self.error_class([ 
                _('Minimum 3 characters required')])
        if not self.instance.check_password(password): 
            self._errors['password'] = self.error_class([ 
                _('Password incorrect')])
        if len(last_name) < 3: 
            self._errors['last_name'] = self.error_class([ 
                _('Minimum 3 characters required')])  
        if notValideEmail(email): 
            self._errors['email'] = self.error_class([ 
                _('Email incorrect')]) 
  
        # return any errors if found 
        return super(UpdateProfileForm, self).clean()

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), 
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save(commit=True)
        # Save many-to-many data
        self.save_m2m()
        return instance