from django.db import models

class Question(models.Model):
    question = models.TextField()
    answer = models.TextField()
    times_tried = models.IntegerField()
    times_right = models.IntegerField()
