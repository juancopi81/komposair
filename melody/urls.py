from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="melody-home"),
    path('generate', views.generate, name="melody-generate"),
    path('save_melody', views.save_melody, name="save-melody")
]
