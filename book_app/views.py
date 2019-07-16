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
		csv_file.close()

		return books

class UploadBookDataView(CreateView):
	model = models.BookData
	form_class = forms.BookDataForm
	template_name = "book_app/create_book_data.html"

	def get_success_url(self, **kwargs): 
		book_form = self.get_form()
		# if book_form.is_valid():
		# 	book_data = book_form.cleaned_data.get('upload')
		# 	for row in book_data:
		# 		print("YO my guy: %s %s"%(row[0], row[3]))
			
		# 	print("Data: %s"%data)
		book_data = models.BookData.objects.all()
		# print("Data %s"%book_data.upload)
		for x in range(len(book_data)):
			if x > 60:
				csv_file = book_data[x].upload
				if csv_file:
					books_reader = csv.reader(csv_file, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
					if books_reader:
						for row in books_reader:
							print("Yo My Guy: %s %s"%(row[0], row[3]))
			

		return reverse_lazy("index")

	def get_context_data(self, **kwargs):
		context = super(UploadBookDataView, self).get_context_data(**kwargs)
		user = self.request.user
		form = self.get_form()
		if user.is_authenticated:
			form.initial['user'] = user.id
			context['book_form'] = form
		return context

	# def post(self, request, *args, **kwargs):
	# 	if not request.user.is_authenticated:
	# 		return HttpResponseForbidden()
	# 	self.object = self.get_object()
	# 	form = self.get_form()
	# 	if form.is_valid():
	# 		return self.form_valid(form, )
	# 	else:
	# 		return self.form_invalid(form)

	# def form_valid(self, form):
	# 	book_object = self.object
	# 	book_csv = book_object.upload
	# 	print("Book CSV: %s"%book_csv)
	# 	books_reader = csv.reader(book_csv, delimiter=str(u',').encode('utf-8'), quotechar=str(u'|').encode('utf-8'))
	# 	for row in books_reader:
	# 		print("Book Row: %s"%row)
	# 	# new_comment = models.Cat_Topic_Comment(
	# 	# 	user = form.cleaned_data['user'],
	# 	# 	cat_topic = form.cleaned_data['cat_topic'],
	# 	# 	comment = form.cleaned_data['comment'],
	# 	# 	comment_picture_path = form.cleaned_data['comment_picture_path']
	# 	# )

	# 	# new_comment.save()
		
	# 	return super(UploadBookDataView, self).form_valid(form)


