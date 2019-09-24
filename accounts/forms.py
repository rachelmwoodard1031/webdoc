from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('User does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('This password is incorrect, please try again')
            if not user.is_active:
                raise forms.ValidationError('User does not have an active account')

        return super(UserLoginForm,self).clean(*args,**kwargs)

class UserRegisterForm(forms.ModelForm):
        email = forms.EmailField(label='Email Address')
        email = forms.EmailField(label='Confirm Email Address')
        password = forms.CharField(widget=forms.PasswordInput)

        class Meta:
            model = User
            fields= [
                'username',
                'email'                   
                'email2',
                'password'
            ]

        def clean_email(self):
            email = self.cleaned_data.get('email')
            email2= self.cleaned_data.get('email2')
            if email != email2:
                raise forms.ValidationError("Emails do not match, try again")
                email_qs= User.objects.filter(email=email)
                if email_qs.exists():
                    raise forms.ValidationError(
                      "An account with this email exists"
                    )
                return email








