import os
import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login

from .models import Choice
from .models import Question
from .models import Survey
from .models import QuestionAnswers
from .models import QuestionChoiceAnswers


class IndexView(generic.ListView):
    template_name = 'index.html'
    def get_queryset(self):
        return Survey.objects.order_by('-start_date')[:5]

def profile(request):
    qa = QuestionAnswers.objects.filter(user=request.user).order_by('question__survey')
    qca = QuestionChoiceAnswers.objects.filter(user=request.user).order_by('question__survey')
    template_name = 'profile.html'
    context = {'qa': qa, 'qca': qca, 'username': request.user.username}
    return render(request, template_name, context)

class DetailView(generic.DetailView):
    model = Survey
    template_name = 'detail.html'


class ResultsView(generic.DetailView):
    model = Survey
    template_name = 'results.html'

def vote(request, question_id):
    survey = get_object_or_404(Survey, pk=question_id)
    
    if request.user.is_anonymous:
        login_ = f'Anon{User.objects.count()+1}'
        user = User.objects.create_user(login_, f'{login}@anon.com', login_)
        login(request, user)
    
    try:
        for question in survey.question_set.all():
            if question.multiple_choice:
                selected_choice = question.choice_set.get(pk=request.POST[question.question_text])
                selected_choice.votes += 1
                selected_choice.save()
                qca = QuestionChoiceAnswers(question=question, user=request.user, answer=selected_choice)
                qca.save()
            else:
                answer = request.POST[question.question_text]
                qa = QuestionAnswers(question=question, user=request.user, answer=answer)
                qa.save()
                
        return HttpResponseRedirect(reverse('api:results', args=(survey.id,)))
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
        
        
def create_user_form(request):
    template_name = 'create_user_form.html'
    return render(request, template_name, {})
        
def create_user(request):
    login_ = request.POST['login']
    password = request.POST['password']
    email = request.POST['email']
    if not login_ or not password or not email:
        return render(request, 'create_user_form.html', {
            'error_message': "You have to fill all the information.",
        })
    try:
        user = User.objects.create_user(login_, email, password)
        login(request, user)
        return render(request, 'create_user_form.html', {
            'error_message': "Created successfully.",
        })
    except IntegrityError:
        return render(request, 'create_user_form.html', {
            'error_message': "The user already exists.",
        })