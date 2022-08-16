from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.donation.models import CustomUser, Donor, Predict
class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
class DonorForm(forms.ModelForm):
    class Meta:
        model =Donor  
        exclude=('user','status','Receive')      


class PredictForm(forms.ModelForm):
    class Meta:
        model = Predict
        fields = ('height','weight')
