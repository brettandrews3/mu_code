from django.contrib import admin
from .models import Question
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
	#fields = ['pub_date', 'question_text']
	fieldsets = [
		# First entry in each tuple == title of that fieldset
		(None,               {'fields': ['question_text']}),
		('Date information', {'fields': ['pub_date']}),
	]

admin.site.register(Question, QuestionAdmin) 