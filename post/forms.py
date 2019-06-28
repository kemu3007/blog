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

    def __init__(self, *args, **kwargs):
        super(CommentCreateForm, self).__init__(*args, **kwargs)
        self.fields['send_by'].initial = 'guest'
        self.fields['contents'].initial = ''
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
