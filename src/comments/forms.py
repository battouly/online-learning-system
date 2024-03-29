from django import forms


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Comment

class CommentForm(forms.Form):
	comment = forms.CharField(
		widget=forms.Textarea(attrs={"placeholder": "Your comment or reply."})
	)

	def __init__(self, data=None, files=None, **kwargs):
		super(CommentForm, self).__init__(data, files, kwargs)
		self.helper 					= FormHelper()
		self.helper.form_show_labels 	= False
		self.helper.add_input(Submit('submit', 'Add Comment', css_class='btn btn-primary',))

class CommentBlogForm(forms.Form):
    content_type 		= forms.CharField(widget=forms.HiddenInput)
    object_id 			= forms.IntegerField(widget=forms.HiddenInput)
    content 			= forms.CharField(label='', widget=forms.Textarea)