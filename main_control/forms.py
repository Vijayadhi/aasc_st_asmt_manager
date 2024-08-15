from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from main_control.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(required=False, widget=forms.PasswordInput,
                                help_text="Leave blank to use the default password.")
    password2 = forms.CharField(required=False, widget=forms.PasswordInput,
                                help_text="Leave blank to use the default password.")

    model = CustomUser
    fields = ('email', 'username', 'mobile_no')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set the default password if none is provided
        if not self.cleaned_data.get("password1"):
            user.set_password('admin')
        if commit:
            user.save()
        return user
    # fields = '__all__'

class CustomUserChangeForm(UserChangeForm):
    model = CustomUser
    fields = ('email', 'username', 'mobile_no')
