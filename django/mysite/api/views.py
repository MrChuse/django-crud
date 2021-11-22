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

from .models import Choice
from .models import Question


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('api:results', args=(question.id,)))
        
def create_user_form(request):
    template_name = 'create_user_form.html'
    return render(request, template_name, {})
        
def create_user(request):
    login = request.POST['login']
    password = request.POST['password']
    email = request.POST['email']
    if not login or not password or not email:
        return render(request, 'create_user_form.html', {
            'error_message': "You have to fill all the information.",
        })
    try:
        user = User.objects.create_user(login, email, password)
        user = authenticate(username=login, password=password)
        if user is not None:
            return HttpResponseRedirect('/admin/')
        return render(request, 'create_user_form.html')
    except IntegrityError:
        return render(request, 'create_user_form.html', {
            'error_message': "The user already exists.",
        })