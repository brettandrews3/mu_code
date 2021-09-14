from django.contrib import admin
from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

# Question has a question and publication date:
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	@admin.display(
		boolean=True,
		ordering='pub_date',
		description='Published recently?',
	)
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now
		#return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	def __str__(self):
		return self.question_text

# Choice has the text of the choice and vote tally:
class Choice(models.Model):
	# ForeignKey ties each Choice to a single Question:
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return self.choice_text