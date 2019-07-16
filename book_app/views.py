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
		print("Current Path %s" %curr_path)
		new_path = os.path.join(curr_path, '..\\static\\csv_files\\books1.csv')
		print("New Path %s" %new_path)
		with open(new_path, 'r') as csv_file:
			print("Hello!!!!!")
			books_reader = csv.reader(csv_file, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
			for row in books_reader:
				print("Row %s"%row)
				book = {
					"book_title": row[0], 
					"book_author": row[1], 
					"date_published": row[2], 
					"book_ID": row[3], 
					"book_publisher": row[4] 
				}

				books.append(book)

		return books


