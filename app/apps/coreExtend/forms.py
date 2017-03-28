from django import forms
from django.forms import widgets, Select
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.utils.translation import ugettext as _, ugettext_lazy as __

from .models import Account

class AccountForm(forms.ModelForm):
    #Assumes that the Account instance passed in has an associated User
    #object. The view (see views.py) takes care of that
    class Meta(object):
        model = Account
        fields = ['location', 'url', 'gender', ]
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs.setdefault('initial', {}).update({'email': instance.email})
        super(AccountForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AccountForm, self).save(commit=commit)
        if 'email' in self.cleaned_data:
            instance.email = self.cleaned_data['email']
            if commit:
                instance.save()
        return instance

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Enter your email address to reset your password"),
        widget=forms.TextInput(attrs={'type':'email', 'class':'form-control', 'placeholder':'Email',}),
        max_length=254,
    )

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()

        # Find users of this email address
        UserModel = get_user_model()
        email = cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(_("Please fill your email address."))
        active_users = UserModel._default_manager.filter(email__iexact=email, is_active=True)

        if active_users.exists():
            # Check if all users of the email address are LDAP users (and give an error if they are)
            found_non_ldap_user = False
            for user in active_users:
                if user.has_usable_password():
                    found_non_ldap_user = True
                    break

            if not found_non_ldap_user:
                # All found users are LDAP users, give error message
                raise forms.ValidationError(_("Sorry, you cannot reset your password here as your user account is managed by another server."))
        else:
            # No user accounts exist
            raise forms.ValidationError(_("This email address is not recognised."))

        return cleaned_data

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
    }
    username = forms.RegexField(
    	label=_("Username"),
    	widget=forms.TextInput(attrs={'type':'text', 'class':'form-control', 'placeholder':'Username',}),
    	max_length=30,
    	regex=r'^[\w-]+$',
    	error_message = _("Usernames must contain only letters, numbers and underscores.")
    )
    password = forms.CharField(
    	label=_("Password"),
    	widget=forms.PasswordInput(attrs={'type':'password', 'class':'form-control', 'placeholder':'Password',})
    )
    email = forms.EmailField(
    	label=_("Email"),
    	widget=forms.TextInput(attrs={'type':'email', 'class':'form-control', 'placeholder':'Email',})
    )

    class Meta:
        model = Account
        fields = ("username", "email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM.
        username = self.cleaned_data["username"]
        try:
            Account._default_manager.get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AccountModelForm(forms.ModelForm):

	class Meta:
		model = Account
		exclude = (
			'username', 'password', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',
			'hide_mobile', 'last_seen_on', 'preferences', 'view_settings', 'send_emails', 'is_beta',
			)
		widgets = {

			#Account
			'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name',}),
			'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name',}),
			'email': forms.TextInput(attrs={'type':'email', 'class':'form-control', 'placeholder':'Email address',}),

			#Profile
			'location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Location',}),
			'url': forms.TextInput(attrs={'type':'url', 'class':'form-control', 'placeholder':'Link to your other website?',}),
			'gender': forms.Select(attrs={'class':'form-control',})
		}
