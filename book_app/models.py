# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class BookData(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=1)
	CSVName = models.CharField(max_length=25, unique=True)
	upload = models.FileField(null=True, blank=True)

	def __str__(self):
		return self.CSVName

