from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import EmailUser


class BaseUserFormMixin(ModelForm):
    """
    Password and confirm password logic
    """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        validate_password(password1)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ManagerUserForm(BaseUserFormMixin):
    """
    Manager-user form 

    todo:
        maybe rename ManagerUserForm and HitmenForm for have only one class?
        but i haven't a good name for that :S
    """

    class Meta:
        model = EmailUser
        fields = ('email', 'first_name', 'last_name')


class HitmenForm(BaseUserFormMixin):
    """
    Hitman-user form 
    """

    class Meta:
        model = EmailUser
        fields = ('email', 'first_name', 'last_name')


class HitmenBossForm(BaseUserFormMixin):
    """
    Hitman-user form for boss interface
    boss can assign managers
    """

    class Meta:
        model = EmailUser
        fields = ('email', 'first_name', 'last_name', 'managed_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['managed_by'].choices = [
            (x.id, x) for x in EmailUser.objects.filter(is_staff=True)]


class HitmenEditForm(ModelForm):
    """
    Hitman-user form 
    """

    class Meta:
        model = EmailUser
        fields = ('email', 'first_name', 'last_name')


class HitmenBossEditForm(ModelForm):
    """
    Hitman-user form for boss interface
    boss can assign managers
    """

    class Meta:
        model = EmailUser
        fields = ('email', 'first_name', 'last_name', 'managed_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['managed_by'].choices = [
            (x.id, x) for x in EmailUser.objects.filter(is_staff=True)]
