from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Region


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "message"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your name or display name",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Share helpful information or your experience...",
                    "rows": 4,
                }
            ),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email address",
            }
        ),
    )

    region = forms.ModelChoiceField(
        queryset=Region.objects.filter(is_active=True).order_by(
            "city",
            "community"
        ),
        empty_label="Select your city and community",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "region",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Choose a username",
                }
            ),
        }