from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate

class SigninTest(TestCase):

	def setUp(self):
		self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
		self.user.save()

	def test_correct_user(self):
		user = authenticate(username='test', password='12test12')
		self.assertTrue((user is not None) and user.is_authenticated)

	def test_wrong_username(self):
		user = authenticate(username='wrong', password='12test12')
		self.assertFalse(user is not None and user.is_authenticated)

	def test_wrong_pssword(self):
		user = authenticate(username='test', password='wrong')
		self.assertFalse(user is not None and user.is_authenticated)

	def test_correct_login_redirct(self):
		c = Client()
		response = c.post('/login/', {'username': 'test', 'password': '12test12'})
		self.assertRedirects(response, '/')

	def test_wrong_login_redirct(self):
		c = Client()
		response = c.post('/login/', {'username': 'test', 'password': '12test123'})
		self.assertTemplateUsed(response, 'users/login.html')