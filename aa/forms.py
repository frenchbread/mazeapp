from models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("user", "rank_score")
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form', 'placeholder': 'Title'}),
            'body': forms.Textarea(attrs={'class': 'form big', 'placeholder': 'Body'}),
        }