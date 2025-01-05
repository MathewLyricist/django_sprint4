from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма для добавления постов."""

    class Meta:
        model = Post
        exclude = (
            'author',
            'is_published',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            ),
        }


class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев."""

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={'rows': '5'}
            )
        }
