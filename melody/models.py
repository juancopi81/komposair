from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Melody(models.Model):
    notes = models.JSONField()
    bpm = models.IntegerField()
    aimodel = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    person = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="melodies")
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)


class Vote(models.Model):

    user_score = models.IntegerField(validators=[MaxValueValidator(1), MinValueValidator(-1)])
    melody = models.ForeignKey(Melody, on_delete=models.CASCADE, related_name="scores")
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="voters")

    def __str__(self):
        return f"{self.person} - {self.melody} - {self.user_score}"


class Comment(models.Model):

    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    melody = models.ForeignKey(Melody, on_delete=models.CASCADE, related_name="comments")
    date_posted = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
