from django.urls import path
from . import views

app_name = 'polls'

# Using Django's generic views to keep URL changes simple, loosely coupled:
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	path('<int:question_id>/vote/', views.vote, name='vote'),
]







"""Here's the original, longform setup for URLs. Compare to production setup above.
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
"""