from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["name", "content"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Título"}),
            "content": forms.Textarea(attrs={"placeholder": "Contenido...", "rows": 10}),
        }