from django import forms
from django.conf import settings

from gymApp.models import CustomUser
from django.contrib.auth.models import Group

from Member.models import * 


#models

class MemberRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Enter First Name"})
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Enter Last Name"})
    )
    age = forms.IntegerField(
        label="Age",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Enter Age"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"})
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )
    
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name", "age", "password", "password_confirm"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs.update({
                    "class": "form-control",
                    "placeholder": field.label
                })
            else:
                field.widget.attrs.update({
                    "class": "form-control"
                })

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # hash password
        if commit:
            user.save()
            member_group, created = Group.objects.get_or_create(name="Member")
            user.groups.add(member_group)
        return user


# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = "__all__"