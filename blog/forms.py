from django import forms
from django.contrib.auth import get_user_model
from .models import Comment, Category, Tag, Post
from django.contrib.auth import forms as auth_forms

User = get_user_model()


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "textarea"})
        }


class PostSearchForm(forms.Form):
    key_word = forms.CharField(
        label="キーワード", required=False,
        widget=forms.TextInput(attrs={"class": "input"}),
        initial = "タイトル、本文"
    )

    category = forms.ModelChoiceField(
        label="キーワード", required=False,
        queryset=Category.objects.all(),
    )

    tags = forms.ModelMultipleChoiceField(
        label="タグの選択", required=False,
        queryset=Tag.objects.all(),
    )

    user = forms.CharField(
        label="投稿者", required=False,
        widget=forms.TextInput(attrs={"class": "input"}),
        initial="投稿者"
    )


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('writer',)


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class LoginForm(auth_forms.AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
