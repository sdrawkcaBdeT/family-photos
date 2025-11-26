from django import forms

class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Family Password',
        'class': 'form-control',
        'autofocus': 'autofocus'
    }))

class NameForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Your Name (e.g. Uncle Bob)',
        'class': 'form-control',
        'autofocus': 'autofocus'
    }))
