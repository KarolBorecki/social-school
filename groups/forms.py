from django import forms

from groups.models import Post, Comment, Group


class PostCreateForm(forms.ModelForm):
    title = forms.CharField()
    text = forms.Textarea()

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
        ]


class CommentCreateForm(forms.ModelForm):
    text = forms.Textarea()

    class Meta:
        model = Comment
        fields = [
            'text',
        ]


class GroupCreateForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.Textarea()

    class Meta:
        model = Group
        fields = [
            'name',
            'description',
        ]
