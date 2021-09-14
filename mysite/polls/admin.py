from django.contrib import admin
from .models import Question
from .models import Choice

class ChoiceInline(admin.TabularInline):
	# 3 choices is the default here. Choices presented in Text/Vote/Delete? lines.
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	#fields = ['pub_date', 'question_text']
	fieldsets = [
		# First entry in each tuple == title of that fieldset
		(None,               {'fields': ['question_text']}),
		('Date information', {'fields': ['pub_date']}),
	]
	inlines = [ChoiceInline] 
	# Choice objects are edited on Question page
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question_text']list_filter

admin.site.register(Question, QuestionAdmin) 
admin.site.register(Choice)