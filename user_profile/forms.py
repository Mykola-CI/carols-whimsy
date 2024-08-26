from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.models import User
from .models import UserProfile


class BasicUserInfoForm(forms.ModelForm):
    # Include first name and last name from the User model
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = UserProfile
        fields = ['profile_title', 'profile_date_of_birth']
        widgets = {
            'profile_date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

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


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_phone_number']
        widgets = {
            'profile_phone_number': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
            })
        }

    def __init__(self, *args, **kwargs):
        super(PhoneNumberForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.profile_phone_number:
            self.fields['profile_phone_number'].widget.attrs['placeholder'] = (
                self.instance.profile_phone_number
            )
        else:
            self.fields['profile_phone_number'].widget.attrs['placeholder'] = (
                'Enter phone number'
            )


class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
            })
        }

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.email:
            self.fields['email'].widget.attrs['placeholder'] = (
                self.instance.email
            )
        else:
            self.fields['email'].widget.attrs['placeholder'] = (
                'Enter email address'
            )


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the FormHelper
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.form_action = '/profile/update/password'

        # Define the layout of the form
        self.helper.layout = Layout(
            'old_password',
            'new_password1',
            'new_password2',
            # Add a submit button with styling
            Submit('submit', 'Change Password', css_class='btn btn-primary')
        )

        # Apply Bootstrap styling to each field
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-lg'
