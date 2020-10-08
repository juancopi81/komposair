from django.db import models
from django.conf import settings
from django.utils import timezone

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