from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.donation.models import CustomUser, Donor
class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
class DonorForm(forms.ModelForm):
    class Meta:
        model =Donor  
        exclude=('user','status','Receive')      
