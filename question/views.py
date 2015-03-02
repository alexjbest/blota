from django.shortcuts import render
from question.models import Question

def index(request):
    rand_q = Question.objects.order_by('?')[0]
    output = rand_q.question

    context = { 'rand_q': rand_q }
    return render(request, 'question/index.html', context)

def file(request, name):
    rand_q = Question.objects.filter(file__name = name).order_by('?')[0]
    output = rand_q.question

    context = { 'rand_q': rand_q }
    return render(request, 'question/index.html', context)
