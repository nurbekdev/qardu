from django import forms
from parler.forms import TranslatableModelForm, TranslatedField
from tinymce.widgets import TinyMCE

from category.models import Category
from oauth.models import Teacher

from .models import Post


class PostForm(TranslatableModelForm):
    title = TranslatedField(
        label="Заголовок",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Заголовок"}
        ),
    )
    body = TranslatedField(
        label="Текст", widget=TinyMCE(attrs={"cols": 80, "rows": 30})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        widget=forms.Select(
            attrs={"class": "form-control selectpicker", "data-live-search": "true"}
        ),
    )
    date = forms.DateField(
        label="Дата",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        label="Преподаватель",
        widget=forms.Select(
            attrs={"class": "form-control selectpicker", "data-live-search": "true"}
        ),
    )
    indexing = forms.CharField(
        label="Индексация",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Индексация"}
        ),
    )

    class Meta:
        model = Post
        fields = ("title", "body", "indexing", "teacher", "category", "date")


class PublicPostForm(TranslatableModelForm):
    title = TranslatedField(
        label="Заголовок",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Заголовок"}
        ),
    )
    body = TranslatedField(
        label="Текст", widget=TinyMCE(attrs={"cols": 80, "rows": 30})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        widget=forms.Select(
            attrs={"class": "form-control selectpicker", "data-live-search": "true"}
        ),
    )
    date = forms.DateField(
        label="Дата",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    indexing = forms.CharField(
        label="Индексация",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Индексация"}
        ),
    )

    class Meta:
        model = Post
        fields = ("title", "body", "indexing", "category", "date")

    def save(self, commit=True):
        return super().save(commit)
