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


class UploadBookDataView(CreateView):
	model = models.BookData
	form_class = forms.BookDataForm
	template_name = "book_app/create_book_data.html"
	
	def get_success_url(self):
		return reverse_lazy('book_app:book_table', kwargs={'pk': self.object.pk})

	# def get_success_url(self, **kwargs): 
			
	# 	# 	print("Data: %s"%data)
	# 	book_data = models.BookData.objects.all()
	# 	# print("Data %s"%book_data.upload)
	# 	curr_length = len(book_data)
	# 	id_is_not_int = False
		
	# 	csv_file = book_data[curr_length-2].upload
	# 	if csv_file:
	# 		books_reader = csv.reader(csv_file, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
	# 		if books_reader:
	# 			for row in books_reader:
	# 				try:
	# 					book_id = int(row[3])
	# 				except:
	# 					book_id = "Not instance"
	# 				if isinstance(book_id, (int)):
	# 					id_is_not_int = False
	# 				else:
	# 					id_is_not_int = True
	# 				print("Is int: %s"%isinstance(book_id, (int)))
	# 				print("Yo My Guy: %s %s"%(row[0], row[3]))
			
	# 	if id_is_not_int:
	# 		return reverse_lazy("book_data:upload", kwargs{'id_is_not_int': id_is_not_int})
	# 	else:
	# 		return reverse_lazy("index", kwargs{'id_is_not_int': id_is_not_int})

	def get_context_data(self, **kwargs):
		context = super(UploadBookDataView, self).get_context_data(**kwargs)
		user = self.request.user
		form = self.get_form()
		if user.is_authenticated:
			form.initial['user'] = user.id
			context['book_form'] = form
		return context


