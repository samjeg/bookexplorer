# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import io
import csv
import tempfile
import urllib
import requests
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
									TemplateView, 
									DetailView,
									CreateView,
									UpdateView,
									DeleteView,
									ListView,
									FormView
								)
from . import models
from . import forms
from bookexplorer import settings


class Register(CreateView):
    form_class = forms.UserCreateForm
    template_name = "book_app/register.html"
    success_url = reverse_lazy("index")

class IndexView(TemplateView):
	template_name = 'book_app/index.html'

class BookTableView(DetailView):
	template_name = 'book_app/book_table.html'
	model = models.BookData

	def get_success_url(self):
		return reverse_lazy('book_app:book_table', kwargs={'pk': self.object.pk})

	def get_context_data(self, **kwargs):
		context = super(BookTableView, self).get_context_data(**kwargs)
		user = self.request.user
		book_obj = self.get_object()
		if user.is_authenticated:
			book_data = self.readBookCSV(book_obj.upload)
			context['book_data'] = book_data
		return context
	

	def readBookCSV(self, csv_file):
		books = []
		books_reader = csv.reader(csv_file, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
		for row in books_reader:
			book = {
				"book_title": row[0], 
				"book_author": row[1], 
				"date_published": row[2], 
				"book_ID": row[3], 
				"book_publisher": row[4] 
			}

			books.append(book)
		csv_file.close()

		return books

class CSVBookListView(ListView):
	template_name = 'book_app/book_list.html'
	model = models.BookData

	def get_context_data(self, **kwargs):
		context = super(CSVBookListView, self).get_context_data(**kwargs)
		user = self.request.user
		if user.is_authenticated:
			context['book_csv_list'] = models.BookData.objects.filter(user=user)
		return context


class UploadBookDataView(FormView):
	model = models.BookData
	form_class = forms.BookDataForm
	template_name = "book_app/create_book_data.html"
	
	# def get_success_url(self):
	# 	return reverse_lazy('book_app:book_table', kwargs={'pk': self.object.pk})

	def get_success_url(self, **kwargs): 
	
					# try:
					# 	book_id = int(row[3])
					# except:
					# 	book_id = "Not instance"
					# if isinstance(book_id, (int)):
					# 	id_is_not_int = False
					# else:
					# 	id_is_not_int = True
					# print("Is int: %s"%isinstance(book_id, (int)))
			
		
		return reverse_lazy("index")

	def get_context_data(self, **kwargs):
		context = super(UploadBookDataView, self).get_context_data(**kwargs)
		user = self.request.user
		form = self.get_form()
		if user.is_authenticated:
			if form.is_valid():
				if not self.id_is_unique:
					context["id_is_not_unique"] = True
			form.initial['user'] = user.id
			context['book_form'] = form
		return context

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		# self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		counter1 = 0
		id_is_unique = True
		self.id_is_unique = True
		csv_file = None
		book_id = "Not instance"
		book_form = self.get_form()
		if book_form.is_valid():
			csv_file = book_form.cleaned_data.get('upload')
			csv_file2 = book_form.cleaned_data.get('upload')
		if csv_file:
			books_reader = csv.reader(csv_file, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
			
			# br_length = sum(1 for line in books_reader)
			if books_reader:
				for row1 in books_reader:
					counter1 = counter1 + 1
					print("counter1: %s"%counter1)
					# print("Row1: %s %s"%(row1[0], row1[3]))
					books_reader2 = csv.reader(csv_file2, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
					counter2 = 0
					for row2 in books_reader2:
						counter2 = counter2 + 1
						print("counter2: %s"%counter2)
						if counter1 != counter2:
							print("Row1 %s Row2 %s"%(row1[3], row2[3]))
							if row1[3] == row2[3]:
								id_is_unique = False
								self.id_is_unique = False
								break
					if not id_is_unique:
						break
					
		
		print("ID Validation %s"%(id_is_unique))			
		
		# new_comment = models.Cat_Topic_Comment(
		# 	user = form.cleaned_data['user'],
		# 	cat_topic = form.cleaned_data['cat_topic'],
		# 	comment = form.cleaned_data['comment'],
		# 	comment_picture_path = form.cleaned_data['comment_picture_path']
		# )

		# new_comment.save()
		if id_is_unique:
			return super(UploadBookDataView, self).form_valid(form)
		else:
			return super(UploadBookDataView, self).form_invalid(form)			


