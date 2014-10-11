from django.shortcuts import render, get_object_or_404
from qanda.models import Answer, Question, Explination

# Create your views here.
def home_page(request):
	return render (request, 'home.html')

def view_question(request, question_id):
	question_stem = Question.objects.get(id=question_id)
	answers = Answer.objects.filter(question=question_stem)
	return render (request, 'view_question.html', {
		'answers': answers, 'question_stem': question_stem
		})

def view_answer(request, question_id):
	question_stem = Question.objects.get(id=question_id)
	next_question_id = int(question_id)+1
	explination_text = get_object_or_404(Explination, question=question_stem)
	correct_answer = Answer.objects.filter(question=question_stem, correct=True)
	return render (request, 'view_answer.html', {
		'correct_answer': correct_answer,
		'question_stem': question_stem,
		'next_question_id':next_question_id,
		'explination_text':explination_text,
		})