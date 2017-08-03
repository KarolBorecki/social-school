from django import forms

from groups.models import Post, Comment


class PostCreateForm(forms.ModelForm):
    title = forms.CharField()
    text = forms.Textarea()

    class Meta:
        model = Post
        fields = [
            'title',
            'text'
        ]


class CommentCreateForm(forms.ModelForm):
    text = forms.Textarea()

    class Meta:
        model = Comment
        fields = [
            'text'
        ]
