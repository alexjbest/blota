from django.shortcuts import render
from question.models import Question

def index(request, name = None, ):
    qs = Question.objects.all()
    if name:
        qs = qs.filter(file__name = name)
    rand_q = qs.order_by('?')[0]
    output = rand_q.question

    context = { 'rand_q': rand_q }
    return render(request, 'question/index.html', context)
