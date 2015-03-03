from django.db import models

class File(models.Model):
    name = models.CharField(max_length = 80)
    preamble = models.TextField()
    def __str__(self):
        return self.name

class Question(models.Model):
    DEFN = 0
    STATE = 1
    PROVE = 2
    TYPE_CHOICES = (
            (DEFN, 'Define'),
            (STATE, 'State'),
            (PROVE, 'Prove'),
            )
    q_type = models.IntegerField(choices = TYPE_CHOICES)
    question = models.TextField()
    answer = models.TextField()
    times_tried = models.IntegerField()
    times_right = models.IntegerField()
    file = models.ForeignKey(File)
    def __str__(self):
        return "%s: %s" % (Question.TYPE_CHOICES[self.q_type][1], self.question)
