from django import forms
from django.forms import extras

from pagedown.widgets import PagedownWidget

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=True))
    publish = forms.DateField(widget=extras.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]