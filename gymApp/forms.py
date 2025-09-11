from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control valid',
        'placeholder': 'Enter your name',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Enter your name'"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control valid',
        'placeholder': 'Email',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Enter email address'"
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Subject',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Enter Subject'"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control w-100',
        'placeholder': 'Enter Message',
        'onfocus': "this.placeholder=''",
        'onblur': "this.placeholder='Enter Message'",
        'cols': 30,
        'rows': 9
    }))