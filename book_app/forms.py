import os
import io
import csv
import tempfile
import urllib
import requests
import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import BookData

class UserCreateForm(UserCreationForm):
	username = forms.EmailField()

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
	upload = forms.FileField()
	id_is_unique = True

	def clean_upload(self):
		csv_file = self.cleaned_data['upload']
		csv_file2 = self.cleaned_data['upload']
		
		counter1 = 0
		self.id_is_unique = True
		if csv_file:
			books_reader = csv.reader(csv_file, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
			
			if books_reader:
				for row1 in books_reader:
					counter1 = counter1 + 1
					if csv_file2:
						books_reader2 = csv.reader(csv_file2, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
						counter2 = 0
						for row2 in books_reader2:
							counter2 = counter2 + 1
							if counter1 != counter2:
								if row1[3] == row2[3]:
									self.id_is_unique = False
									raise forms.ValidationError("CSV file does not have a unique id's")
		
	
		return csv_file	
		

	class Meta:
		fields = ("user", "upload")
		model = BookData


	def __init__(self, *args, **kwargs):
		super(BookDataForm, self).__init__(*args, **kwargs)
		self.fields['upload'].help_text = None 
	


