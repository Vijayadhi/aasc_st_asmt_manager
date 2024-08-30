from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from clg_admin.models import Faculty
from main_control.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(required=False, widget=forms.PasswordInput,
                                help_text="Leave blank to use the default password.")
    password2 = forms.CharField(required=False, widget=forms.PasswordInput,
                                help_text="Leave blank to use the default password.")

    model = CustomUser
    fields = ('email', 'name', 'mobile_no')

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
    fields = '__all__'


class FacultyAdminForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        widgets = {
            'faculty_type': FilteredSelectMultiple("Roles", is_stacked=False),  # Custom widget for multi-select
        }