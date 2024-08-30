from django import forms
from clg_admin.models import LeaveLetter, Faculty


class LeaveLetterAdminForm(forms.ModelForm):
    class Meta:
        model = LeaveLetter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(args)
        # Get the current user from the request
        if 'request' in kwargs:
            request = kwargs['request']
            # Filter faculty objects based on the current user
            # Assuming the Faculty model has a ForeignKey to User
            user_faculty = Faculty.objects.filter(user=request.user).first()
            print(user_faculty)
            if user_faculty:
                self.fields['faculty'].queryset = Faculty.objects.filter(id=user_faculty.id)
            else:
                self.fields['faculty'].queryset = Faculty.objects.none()