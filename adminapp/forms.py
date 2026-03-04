from django import forms
from app1.models import Turf 

class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control shadow-sm",
            "placeholder": "Enter admin email"
        })
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control shadow-sm",
            "placeholder": "Enter password"
        })
    )


class TurfForm(forms.ModelForm):
    class Meta:
        model = Turf
        fields = "__all__"

