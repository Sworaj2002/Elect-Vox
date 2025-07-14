from django import forms
from .models import User, RegisterCandidate
from datetime import date

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'date_of_birth', 'aadhar', 'password', 'confirm_password']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists")
        return phone_number

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return dob

class LoginForm(forms.Form):
    email_or_phone = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

class CandidateRegistrationForm(forms.ModelForm):
    class Meta:
        model = RegisterCandidate
        fields = ['full_name', 'photo', 'aadhar_number', 'voter_id', 'manifesto', 'supporters_names']
