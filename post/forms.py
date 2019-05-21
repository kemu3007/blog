from django import forms

from .models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('send_by', 'contents')
        widgets = {
            'post': forms.ChoiceField(),
            'send_by': forms.TextInput(attrs={'size': 40}),
            'contents': forms.Textarea()
        }
