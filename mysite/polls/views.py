from django.shortcuts import render
#from django.http import HttpResponse      (Now handled by importing get_object_or_404)
#from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Question
from .models import Choice

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
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
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
# This is the long-form def detail(). The production one above uses shortcuts.
def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("This question doesn't exist.")
	return render(request, 'polls/detail.html', {'question': question})
	#return HttpResponse("You're looking at question %s." % question_id)
"""