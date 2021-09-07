import datetime
from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() should return False for questions
		whose pub_date is still in the future:
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() should return False for questions whose
		pub_date is older than 1 day:
		"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() should return True for questions whose
		pub_date occurred within the last 24 hours:
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

# Here, we'll add some tests for questions outside of this 24 hour period:

def create_question(question_text, days):
	"""
	Create a question with the given 'question_text' and publish the given
	number of 'days' offset to now (negative for questions in the past, positive 
	for questions that haven't been published yet).
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question.text, pub_date=time)

class QuestionIndexViewTests(TestCase):
	def test_no_questions(self):
		# No questions exist? Display the appropriate message:
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_past_question(self):
		# Quesions with a pub_date in the past show up on the index page:
		question = create_question(question_text="Past question,", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[question],
		)

	def test_future_question(self):
		# Questions with future pub_date aren't shown on the index page.
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_future_question_and_past_question(self):
		# Only show past questions, even if future questions exist, too.
		question = create_question(question_text="Past question.", days=-30)
		create_question(question_text = "Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[question],
		)

	def test_two_past_questions(self):
		# Questions index page may display multiple entries.
		question1 = create_question(question_text="Past question 1.", days=-30)
		question2 = create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			[question2, question1],
		)