from django import forms
from .models import Issue, Comment, Community


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'category', 'community', 'location', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Brief summary of the issue'}),
            'location': forms.TextInput(attrs={'placeholder': 'Street, landmark, or specific junction'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Detailed description of what needs attention...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['community'].empty_label = "Select Community / Neighborhood"
        self.fields['community'].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Share an update, progress report, or note...',
            }),
        }
        labels = {
            'content': 'Add a Comment',
        }