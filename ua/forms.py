from django import forms
from views import Member

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = {'user', }
        widgets = {
            'website': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Web-site'}),
            'location': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Location'}),
            'bio': forms.Textarea(attrs={'class': 'form big', 'placeholder': 'Bio'}),
        }