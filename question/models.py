from django.db import models

class File(models.Model):
    name = models.CharField(max_length = 80)
    preamble = models.TextField()
    def __str__(self):
        return self.name

class Question(models.Model):
    DEFN = 'D'
    STATE = 'S'
    PROVE = 'P'
    TYPE_CHOICES = (
            (DEFN, 'Definition'),
            (STATE, 'State'),
            (PROVE, 'Prove'),
            )
    q_type = models.CharField(max_length = 1, choices = TYPE_CHOICES, default = STATE)
    question = models.TextField()
    answer = models.TextField()
    times_tried = models.IntegerField()
    times_right = models.IntegerField()
    file = models.ForeignKey(File)
    def __str__(self):
        return self.question
