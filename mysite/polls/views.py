from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Question
from .models import Choice

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""
		Return last 5 published questions, exluding those set
		to publish in the future:
		"""
		return Question.objects.filter(
			pub_date__lte=timezone.now() 
			).order_by('-pub_date')[:5]
		# OLD: Returns the last five published questions:
		# return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	def get_queryset(self):
		# Exclude questions that aren't published yet.
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	#return HttpResponseRedirect("You're voting on question %s." % question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplays the question voting form
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# You want to always return an HttpResponseRedirect after successfully
		# dealing with POST data. This prevents data from being submitted a second
		# time if the user hits the Back button on their browser.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))














"""
# Here's the original views for index, detail, and results.
# The views used above employe Django's generic views for simplicity's sake.
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)

# This detail() uses get_object_or_404() to maintain loose coupling,
# whereas using the detail() shown below ties the model layer to the view layer.
def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})
"""