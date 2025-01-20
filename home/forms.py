from home.models import ContactMessage
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class':'input','placeholder':'John' }),
            'subject': forms.TextInput(attrs={'class':'input','placeholder':'Subject'}),
            'email': forms.TextInput(attrs={'class':'input', 'placeholder': 'example@domain.com'}),
            'message': forms.Textarea(attrs={'class':'input', 'placeholder':'Your quetions or comments', 'rows':'5'}),
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'subject',
            'email',
            'message',
        )
        self.helper.add_input(Submit('save', 'submit', css_class = 'btn-primary'))

        super(ContactForm,self).__init__(*args, **kwargs)

class SearchForm(forms.Form):
    query = forms.CharField(max_length=50)
    catid = forms.IntegerField()
    
   
