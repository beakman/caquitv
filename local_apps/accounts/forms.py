from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile
from accounts.models import UserProfile

attrs_dict = { 'class': 'required' }

class RegistrationFormZ(RegistrationForm):
    url = forms.URLField()
    avatar = forms.ImageField()

    def save(self, profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
        password=self.cleaned_data['password1'],
        email=self.cleaned_data['email'])

        new_profile = UserProfile(
            user=new_user, 
            url = self.cleaned_data['url'],
            avatar = self.cleaned_data['avatar']
            )
        new_profile.save()

        return new_user

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField()

    def __init__(self, *args, **kw):
        super(forms.ModelForm, self).__init__(*args, **kw)
        self.fields['email'].initial = self.instance.user.email
        self.fields.keyOrder = [
            'url',
            'email',
            'avatar'
            ]

    class Meta:
        model = UserProfile
        exclude=('user', 'karma', 'episodes_submited')
    
    def save(self, *args, **kw):
        super(forms.ModelForm, self).save(*args, **kw)
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()
        profile = super(UserProfileForm, self).save(*args,**kw)
        return profile


