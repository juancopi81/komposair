from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="melody-home"),
    path('generate', views.generate, name="melody-generate")
]
