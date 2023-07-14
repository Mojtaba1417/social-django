from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'none'}))
    password2 = forms.CharField(label='تایید پسورد',widget=forms.PasswordInput(attrs={'required': 'none'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError('شما قبلا با این ایمیل ثبت نام کرده اید .')
        return email

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("passwords not matched")

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("از جون سایت چی میخوایی؟؟؟؟؟؟")
        return username


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'none', 'class': 'form-control'}))


class EditUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('age', 'bio')