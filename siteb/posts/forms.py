from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget)
	publish = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model = Post
		fields = [
			"title",
			"content",
			"image",
			"height_field",
			"width_field",
			"draft",
			"publish",
			
		]