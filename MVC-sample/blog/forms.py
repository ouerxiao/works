from django import forms
from blog.models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment']
        widgets = {
            'subject': forms.TextInput(attrs={'class':'input', 'placeholder':'subject'}),
            'comment': forms.Textarea(attrs={'class':'input', 'placeholder':'comment', 'rows':'5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'subject',
            'comment',
        )

