from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from forums.models import Profile


# invite code form



# Update Profile Form
class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("fullname", "bio", "role", "profile_pic")