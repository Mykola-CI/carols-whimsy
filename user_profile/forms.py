from django import forms
from .models import UserProfile


class BasicUserInfoForm(forms.ModelForm):
    # Include first name and last name from the User model
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = UserProfile
        fields = ['profile_title', 'profile_date_of_birth']

    def __init__(self, *args, **kwargs):
        # Retrieve the User instance and remove it from kwargs
        # because ModelForm doesn't expect it and may raise an error
        user = kwargs.pop('user', None)
        super(BasicUserInfoForm, self).__init__(*args, **kwargs)

        # Set initial values for first name and last name if user is provided
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

        # Set placeholders and classes for the form fields
        placeholders = {
            'profile_date_of_birth': (
                self.instance.profile_date_of_birth or 'DD-MM-YYYY'
            ),
            'profile_title': self.instance.profile_title or 'Title',
            'first_name': user.first_name or 'First Name',
            'last_name': user.last_name or 'Last Name',
        }

        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = (
                placeholders[field]
            )
            self.fields[field].widget.attrs['class'] = (
                'form-control form-control-lg'
            )

    # Override the save method to update the User and the UserProfile instances
    # because I deal with two models here, whereas the form is bound for one
    def save(self, commit=True):
        # Save the UserProfile instance
        user_profile = super(BasicUserInfoForm, self).save(commit=False)

        # Update the User instance
        user = user_profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            user_profile.save()

        return user_profile
