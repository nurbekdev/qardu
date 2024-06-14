from django import forms
from parler.forms import TranslatableModelForm, TranslatedField
from tinymce.widgets import TinyMCE

from category.models import Category
from oauth.models import Teacher

from .models import Post, Document

class PostForm(TranslatableModelForm):
    title = TranslatedField(
        label="Sarlavha",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Sarlavha"}
        ),
    )
    body = TranslatedField(
        label="Matn", widget=TinyMCE(attrs={"cols": 80, "rows": 30})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Kategoriya",
        widget=forms.Select(
            attrs={"class": "form-select", "data-live-search": "true"}
        ),
    )
    date = forms.DateField(
        label="Sana",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        label="O'qituvchi",
        widget=forms.Select(
            attrs={"class": "form-select", "data-live-search": "true"}
        ),
    )
    indexing = forms.CharField(
        label="Indeksatsiya",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Indeksatsiya"}
        ),
    )
    file = forms.FileField(
        label="Fayl",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Post
        fields = ("title", "body", "indexing", "teacher", "category", "date", "file")


class PublicPostForm(TranslatableModelForm):
    title = TranslatedField(
        label="Sarlavha",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Sarlavha"}
        ),
    )
    body = TranslatedField(
        label="Matn", widget=TinyMCE(attrs={"cols": 80, "rows": 30})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Kategoriya",
        widget=forms.Select(
            attrs={"class": "form-select", "data-live-search": "true"}
        ),
    )
    date = forms.DateField(
        label="Sana",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    indexing = forms.CharField(
        label="Indeksatsiya",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Indeksatsiya"}
        ),
    )
    file = forms.FileField(
        label="Fayl",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Post
        fields = ("title", "body", "indexing", "category", "date", "file")

    def save(self, commit=True):
        post = super().save(commit)
        if self.cleaned_data['file']:
            Document.objects.create(post=post, file=self.cleaned_data['file'])
        return post
