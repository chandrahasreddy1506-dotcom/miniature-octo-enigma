import re
from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    citizen_phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number (Optional)'})
    )

    class Meta:
        model = Issue
        fields = ['title', 'department', 'location', 'citizen_phone', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Broken water pipe on Main Road', 'required': True}),
            'department': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3rd Cross, near Community Hall', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the civic problem in detail...', 'required': True}),
        }

    def clean_citizen_phone(self):
        phone = (self.cleaned_data.get('citizen_phone') or '').strip()
        if phone:
            if not re.match(r'^\+?[0-9]{10,15}$', phone):
                raise forms.ValidationError("Enter a valid phone number (10 to 15 digits).")
        return phone