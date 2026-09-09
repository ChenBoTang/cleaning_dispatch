
from django import forms
from django.contrib.auth.models import User

from .models import (
    Customer,
    Vehicle,
    Employee,
    Job,
    Dispatch,
)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "contact",
            "phone",
            "address",
            "note",
        ]


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "plate_no",
            "name",
            "vehicle_type",
            "status",
            "note",
        ]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "name",
            "phone",
            "position",
            "available",
            "note",
        ]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "job_no",
            "customer",
            "clean_date",
            "clean_time",
            "address",
            "clean_type",
            "status",
            "note",
        ]

        widgets = {
            "clean_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
            "clean_time": forms.TimeInput(
                attrs={
                    "type": "time"
                }
            ),
        }


class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = [
            "job",
            "vehicle",
            "driver",
            "cleaner",
            "departure_time",
            "return_time",
            "status",
            "note",
        ]

        widgets = {
            "departure_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),
            "return_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),
        }


# ============================================================
# 會員註冊表單
# ============================================================

class CustomerRegistrationForm(forms.Form):
    username = forms.CharField(
        label="會員帳號",
        max_length=150
    )

    email = forms.EmailField(
        label="Email"
    )

    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput
    )

    name = forms.CharField(
        label="姓名",
        max_length=100
    )

    contact = forms.CharField(
        label="聯絡人",
        max_length=100,
        required=False
    )

    phone = forms.CharField(
        label="電話",
        max_length=30,
        required=False
    )

    address = forms.CharField(
        label="地址",
        max_length=255,
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "這個帳號已經有人使用。"
            )

        return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if (
            password
            and password_confirm
            and password != password_confirm
        ):
            raise forms.ValidationError(
                "兩次輸入的密碼不一致。"
            )

        return cleaned_data

