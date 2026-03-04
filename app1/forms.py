from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser
from .models import Booking
from datetime import datetime, timedelta,date

from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    class Meta:
        model = CustomUser   
        fields = ["email", "username", "password1", "password2"]  
        

        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(  
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['date', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        """
        Clean, optimized initialization without changing functionality.
        """
        super().__init__(*args, **kwargs)

        # ------------------------------
        # 1. Prevent selecting past dates
        # ------------------------------
        today_str = date.today().strftime('%Y-%m-%d')
        self.fields['date'].widget = forms.DateInput(
            attrs={'type': 'date', 'min': today_str}
        )

        # ------------------------------------
        # 2. Start-time choices (6 AM → 1 AM)
        # ------------------------------------
        # hours 6 → 23, then 0 (midnight)
        time_hours = list(range(6, 24)) + [0]
        time_choices = [
            (f"{h:02d}:00", f"{h:02d}:00")
            for h in time_hours
        ]

        self.fields['start_time'] = forms.ChoiceField(choices=time_choices)

        # -------------------------------
        # 3. End time – auto-filled + read-only
        # -------------------------------
        self.fields['end_time'].widget = forms.TextInput(
            attrs={'readonly': 'readonly'}
        )

        # --------------------------------------
        # 4. Set initial end_time if start exists
        # --------------------------------------
        start_time = self.initial.get('start_time')

        if start_time:
            self.initial['end_time'] = self._calculate_end_time(start_time)
        else:
            self.initial.setdefault('end_time', '')

    # ==========================================================
    # Utility function to clearly calculate end time (+1 hour)
    # ==========================================================
    def _calculate_end_time(self, start_time):
        try:
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = start_dt + timedelta(hours=1)
            return end_dt.strftime("%H:%M")
        except Exception:
            # safe fallback, does NOT break functionality
            return "07:00"

    # ==========================================================
    # Clean method – ensures end_time always updates correctly
    # ==========================================================
    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        if start_time:
            end_time = self._calculate_end_time(start_time)

            # Auto-set end_time in cleaned data (not user input)
            cleaned_data['end_time'] = end_time
        else:
            self.add_error('start_time', 'Invalid start time.')

        return cleaned_data