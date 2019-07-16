# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import csv
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


class Register(CreateView):
    form_class = forms.UserCreateForm
    template_name = "book_app/register.html"
    success_url = reverse_lazy("index")

class IndexView(TemplateView):
	template_name = 'book_app/index.html'

class BookTableView(TemplateView):
	template_name = 'book_app/book_table.html'

	def get_context_data(self, **kwargs):
		context = super(BookTableView, self).get_context_data(**kwargs)
		user = self.request.user
		if user.is_authenticated:
			book_data = self.readBookCSV()
			context['book_data'] = book_data
		return context
	

	def readBookCSV(self):
		books = []
		curr_path = os.path.dirname(__file__)
		new_path = os.path.join(curr_path, '..\\static\\csv_files\\books1.csv')
		with open(new_path, 'r') as csv_file:
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

		return books

class UploadBookDataView(CreateView):
	model = models.BookData
	form_class = forms.BookDataForm
	template_name = "book_app/create_book_data.html"
	success_url = reverse_lazy("index")

	def get_context_data(self, **kwargs):
		context = super(UploadBookDataView, self).get_context_data(**kwargs)
		user = self.request.user
		form = self.get_form()
		if user.is_authenticated:
			form.initial['user'] = user.id
			context['book_form'] = form
		return context

