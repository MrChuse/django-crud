from django.db import models
from django.contrib.auth import models as a_models

class Survey(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def __str__(self):
        return self.name

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    multiple_choice = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text

class QuestionAnswers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(a_models.User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question.question_text +' '+self.answer

class QuestionChoiceAnswers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(a_models.User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE)
    def __str__(self):
        return self.question.question_text +' '+self.answer.choice_text