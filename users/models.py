# See https://blog.eepy.net/2020/06/15/starting-a-django-project-with-the-right-user-model/
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from PIL import Image


class User(AbstractUser):
    """auth/login-related fields"""
    pass
    # Examples:
    # email (if used for login)
    # extra permissions
    # NOTE: before putting something here make sure it wouldn't be better in the profile model


class Profile(models.Model):
    """non-auth-related/cosmetic fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Custom information to add no required
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    country = CountryField(blank=True)
    bio = models.CharField(max_length=500, blank=True)
    name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):

        # Run save method of paren
        super().save(*args, **kwargs)

        # Get the image of the user
        img = Image.open(self.image.path)

        # Resize if neccesary
        if img.height > 300 or img.width > 300:
            output_size = [300, 300]
            img.thumbnail(output_size)
            img.save(self.image.path)

    # Examples:
    # Display Name
    # Bios, descriptions, taglines
    # Theme (light or dark)
    # email (if not used to log in)
