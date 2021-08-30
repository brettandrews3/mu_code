from django.urls import path
from . import views

urlpatterns = [
	# ex: /polls/
	path('', views.index, name='index'),
	# Here's the 'name' value that's called by {% url %} template tag in index.html:
	path('<int:question_id>/', views.detail, name='detail'),
	# ex: /polls/5/results/
	path('<int:question_id>/results/', views.results, name='results'),
	# ex: /polls/5/vote/
	path('<int:question_id>/vote/', views.vote, name='vote'),
]