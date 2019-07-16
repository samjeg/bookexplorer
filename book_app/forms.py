from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import BookData

class UserCreateForm(UserCreationForm):

	class Meta:
		fields = ("username", "password1", "password2")
		model = get_user_model()

	def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)
		self.fields["username"].label = "Username:"
		self.fields["username"].help_text = None
		self.fields["password1"].help_text = None
		self.fields["password2"].help_text = None


class BookDataForm(forms.ModelForm):
	user = forms.ModelChoiceField(widget = forms.HiddenInput(), queryset=User.objects.all())
	CSVName = forms.CharField()
	CSVURL = forms.URLField()
	upload = forms.FileField()

	class Meta:
		fields = ("user", "CSVName", "CSVURL", "upload")
		model = BookData
