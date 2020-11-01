from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Sum
from .models import Melody, Vote, Comment

notes = {
	"m1": '[{"pitch": 60, "velocity": 90, "startTime": 0, "endTime": 0.666667, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 64, "velocity": 90, "startTime": 0.666667, "endTime": 1.333334, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 64, "velocity": 90, "startTime": 1.333334, "endTime": 2.000001, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 60, "velocity": 90, "startTime": 2.000001, "endTime": 2.666668, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 59, "velocity": 90, "startTime": 2.666668, "endTime": 3.333335, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 57, "velocity": 90, "startTime": 3.333335, "endTime": 4.000002, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 55, "velocity": 90, "startTime": 4.000002, "endTime": 4.666669, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 59, "velocity": 90, "startTime": 4.666669, "endTime": 5.333336, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 62, "velocity": 90, "startTime": 5.333336, "endTime": 6.000003, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 62, "velocity": 90, "startTime": 6.000003, "endTime": 6.66667, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 60, "velocity": 90, "startTime": 6.66667, "endTime": 7.333337, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 59, "velocity": 90, "startTime": 7.333337, "endTime": 8.000004, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 60, "velocity": 90, "startTime": 8.000004, "endTime": 9.333338, "instrument": 0, "program": 0, "isDrum": false}]',
	"m2": '[{"pitch": 72, "velocity": 90, "startTime": 0, "endTime": 0.666666, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 67, "velocity": 90, "startTime": 0.666666, "endTime": 1.333332, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 64, "velocity": 90, "startTime": 1.333332, "endTime": 1.999998, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 72, "velocity": 90, "startTime": 1.999998, "endTime": 2.666664, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 71, "velocity": 90, "startTime": 2.666664, "endTime": 3.33333, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 67, "velocity": 90, "startTime": 3.33333, "endTime": 3.999996, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 64, "velocity": 90, "startTime": 3.999996, "endTime": 4.666662, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 71, "velocity": 90, "startTime": 4.666662, "endTime": 5.333328, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 72, "velocity": 90, "startTime": 5.333328, "endTime": 5.999994, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 67, "velocity": 90, "startTime": 5.999994, "endTime": 6.66666, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 64, "velocity": 90, "startTime": 6.66666, "endTime": 7.333326, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 72, "velocity": 90, "startTime": 7.333326, "endTime": 7.999992, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 69, "velocity": 90, "startTime": 7.999992, "endTime": 8.666658, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 67, "velocity": 90, "startTime": 8.666658, "endTime": 9.333324, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 65, "velocity": 90, "startTime": 9.333324, "endTime": 9.99999, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 64, "velocity": 90, "startTime": 9.99999, "endTime": 10.666656, "instrument": 0, "program": 0, "isDrum": false}]',
	"m3": '[{"pitch": 69, "velocity": 90, "startTime": 0, "endTime": 0.4166665, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 64, "velocity": 90, "startTime": 0.4166665, "endTime": 0.833333, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 69, "velocity": 90, "startTime": 0.833333, "endTime": 1.666666, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 69, "velocity": 90, "startTime": 1.666666, "endTime": 2.0833325, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 2.0833325, "endTime": 2.499999, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 2.499999, "endTime": 2.9166655, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 75, "velocity": 90, "startTime": 2.9166655, "endTime": 3.333332, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 3.333332, "endTime": 4.166665, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 4.5833315, "endTime": 4.999998, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 4.999998, "endTime": 5.62499775, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 77, "velocity": 90, "startTime": 5.62499775, "endTime": 5.833331, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 74, "velocity": 90, "startTime": 5.833331, "endTime": 6.2499975, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 6.2499975, "endTime": 6.666664, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 74, "velocity": 90, "startTime": 6.666664, "endTime": 7.29166375, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 74, "velocity": 90, "startTime": 7.29166375, "endTime": 7.499997, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 7.499997, "endTime": 7.9166635, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 72, "velocity": 90, "startTime": 7.9166635, "endTime": 8.33333, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 77, "velocity": 90, "startTime": 8.33333, "endTime": 9.166663, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 9.166663, "endTime": 9.5833295, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 77, "velocity": 90, "startTime": 9.5833295, "endTime": 9.999996, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 79, "velocity": 90, "startTime": 9.999996, "endTime": 10.4166625, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 10.4166625, "endTime": 10.833328999999999, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 76, "velocity": 90, "startTime": 10.833328999999999, "endTime": 11.2499955, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 74, "velocity": 90, "startTime": 11.2499955, "endTime": 11.666662, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 74, "velocity": 90, "startTime": 11.666662, "endTime": 12.0833285, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 72, "velocity": 90, "startTime": 12.0833285, "endTime": 12.499995, "instrument": 0, "program": 0, "isDrum": false}, {"pitch": 71, "velocity": 90, "startTime": 12.499995, "endTime": 13.124994749999999, "instrument": 0, "program": 0, "isDrum": false}]' 
}

class MelodyTestCase(TestCase):

	def setUp(self):

		# Create user
		self.user = get_user_model().objects.create_user(username="test", password="12test12", email="test@example.com")
		self.user.save()

		user = authenticate(username="test", password="12test12")

		# Create Melodies
		m1 = Melody.objects.create(notes=notes["m1"], bpm =90, aimodel="lstm_folk_1", score=0)
		m1.person.add(user)
		m2 = Melody.objects.create(notes=notes["m2"], bpm =78, aimodel="magenta-melody_rnn", score=2)
		m2.person.add(user)
		m3 = Melody.objects.create(notes=notes["m3"], bpm =90, aimodel="lstm_folk_1", score=-1)
		m3.person.add(user)

		# Create votes
		v1 = Vote.objects.create(user_score=1, melody=m1, person=user)
		v2 = Vote.objects.create(user_score=0, melody=m2, person=user)
		v3 = Vote.objects.create(user_score=-1, melody=m3, person=user)
		v4 = Vote.objects.create(user_score=2, melody=m1, person=user)

		# Create comments
		c1 = Comment.objects.create(posted_by=user, melody=m1, comment="I like this melody")
		c2 = Comment.objects.create(posted_by=user, melody=m2, comment="I do not like this melody")
		c3 = Comment.objects.create(posted_by=user, melody=m3, comment="I love this melody")

	def test_melodies_count(self):
		user = authenticate(username="test", password="12test12")
		self.assertEqual(user.melodies.count(), 3)

	def test_votes_count(self):
		user = authenticate(username="test", password="12test12")
		self.assertEqual(user.voters.count(), 4)

	def test_comments_count(self):
		user = authenticate(username="test", password="12test12")
		self.assertEqual(user.reviews.count(), 3)

	def test_melody_scores_count(self):
		melody = Melody.objects.get(notes=notes["m1"])
		self.assertEqual(melody.scores.count(), 2)

	def test_melody_comments_count(self):
		melody = Melody.objects.get(notes=notes["m1"])
		self.assertEqual(melody.comments.count(), 1)
