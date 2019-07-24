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
	upload = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))
	id_is_unique = True

	def clean_upload(self):
		csv_file = self.cleaned_data['upload']
		csv_file2 = self.cleaned_data['upload']
		
		counter1 = 0
		self.id_is_unique = True

		# print("Hello clean upload")
		# Nested loop to to check each row id is unique
		if csv_file:
			books_reader = csv.reader(csv_file, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
			# print("Hello csv file")

			if books_reader:
				# print("Hello book reader")

				
				for row1 in books_reader:
					counter1 = counter1 + 1
					# print("Hello row %s"%row1)

					
					if csv_file2:
						books_reader2 = csv.reader(csv_file2, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
						counter2 = 0
						# print("Hello csv_file2")

						
						for row2 in books_reader2:
							counter2 = counter2 + 1
							# print("Hello row2 %s"%row2)
							
							if counter1 != counter2:
								# print("Hello counter1 %s"%counter1)

								
								if row1[3] == row2[3]:
									self.id_is_unique = False
									raise forms.ValidationError("CSV file does not have a unique id's")
		
		# csv file size max 3KB
		if csv_file.size > 3000:
			raise forms.ValidationError("CSV file is too large")
		
		# csv colomn
		row_counter = 0
		if csv_file:
			col_books_reader = csv.reader(csv_file, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
			# print("Hello csv file")

			if col_books_reader:

				for book_row in col_books_reader:
					col_amount = len(book_row)
					print("Coloumn amount %s"%col_amount)

					if col_amount > 5 or col_amount < 5:
						raise forms.ValidationError("Wrong number of columns in csv file")				
	
		return csv_file

				

	class Meta:
		fields = ("user", "upload")
		model = BookData
	


