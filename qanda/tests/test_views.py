from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from qanda.views import home_page, check_answer
from qanda.models import Answer, Question, Explanation, Reference
from django.shortcuts import get_object_or_404

class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page(self):
		address = resolve('/')
		self.assertEqual(address.func, home_page)

	# def test_home_page_returns_correct_html(self):
	# 	request = HttpRequest()
	# 	response = home_page(request)
	# 	expected_html = render_to_string('home.html')
	# 	self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_renders_home_template(self):
		Question.objects.create()
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

class QuestionViewTest (TestCase):

	def test_uses_view_template(self):
		question_stem = Question.objects.create()
		Answer.objects.create(text='',question=question_stem, correct=True)
		response = self.client.get('/questions/%d/' % (question_stem.id,))
		self.assertTemplateUsed(response, 'view_question.html')

	def test_displays_answers_only_for_that_question(self):
		correct_question = Question.objects.create(text="Question #1: This is the first question ever")
		Answer.objects.create(text="Answer 1", question=correct_question, correct=True)
		Answer.objects.create(text="Answer 2", question=correct_question, correct=False)
		Explanation.objects.create(text='Explanation #1', question=correct_question)
		Reference.objects.create(text='Reference #1', question=correct_question)	

		other_question = Question.objects.create()
		Answer.objects.create(text="Other Answer 1", question=other_question)
		Answer.objects.create(text="Other Answer 2", question=other_question)
		
		response = self.client.get('/questions/%d/' % (correct_question.id,))

		saved_answers = Answer.objects.all()

		self.assertContains(response, 'Answer 1')
		self.assertContains(response, 'Question #1')
		self.assertNotContains(response, 'Other Answer')
		self.assertTrue(saved_answers[0])

	def test_question_view_page_can_save_a_POST_request(self):
		question_stem = Question.objects.create()
		correct_answer = Answer.objects.create(text='Test radio answer',question=question_stem, correct=True)

		request = HttpRequest()
		request.method = 'POST'
		request.POST['radio_answer'] = 'Test radio answer'
		user_answer = request.POST['radio_answer']

		response = check_answer(request, '1')

		self.assertEqual(correct_answer.text, user_answer)

class AnswerViewTest (TestCase):
	
	def test_uses_view_template(self):
		question_stem = Question.objects.create()
		Explanation.objects.create(text='Correct Explanation', question=question_stem)
		question_stem.save()
		response = self.client.get('/questions/%d/answer' % (question_stem.id,))
		self.assertTemplateUsed(response, 'view_answer.html')

	def test_displays_question_stem_and_correct_answer_only(self):
		correct_question = Question.objects.create(text="Question #1: This is the first question ever")
		Answer.objects.create(text="Answer 1", question=correct_question, correct=True)
		Answer.objects.create(text="Answer 2", question=correct_question, correct=False)
		Explanation.objects.create(text='Correct Explanation', question=correct_question)
		
		response = self.client.get('/questions/%d/answer' % (correct_question.id,))

		self.assertContains(response, 'Answer 1')
		self.assertNotContains(response, 'Answer 2')

	def test_displays_correct_Explanation(self):
		correct_question = Question.objects.create(text="Q1")
		wrong_question = Question.objects.create(text="Q2")
		Answer.objects.create(text='Answer 1', question=correct_question)
		Answer.objects.create(text='Answer 2', question=correct_question)
		Answer.objects.create(text='Other answer 1', question=wrong_question)
		Explanation.objects.create(text='Correct Explanation', question=correct_question)
		Explanation.objects.create(text='Wrong Explanation', question=wrong_question)

		Explanation_text = Explanation.objects.get(question=correct_question)
		self.assertEqual('Correct Explanation', Explanation_text.text)

	def test_retrieve_correct_reference(self):
		correct_question = Question.objects.create(text="Q1")
		Reference.objects.create(text='Reference #1', question=correct_question)

		reference_text = get_object_or_404(Reference, question=correct_question)
		
		self.assertEqual('Reference #1', reference_text.text)



