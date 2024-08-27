from django.db import models

class QuizQuestion(models.Model):
    T_ID = models.IntegerField()
    question_type = models.CharField(max_length=100)
    question = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)