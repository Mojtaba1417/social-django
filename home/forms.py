from django import forms
from . models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control col-md-6' , 'rows': 10, 'resize': 'none'})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control col-md-6' , 'rows': 10, 'resize': 'none'})
        }

class PosrSearchForm(forms.Form):
    search = forms.CharField()