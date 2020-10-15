from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="melody-home"),
    path('generate', views.generate, name="melody-generate"),
    path('save_melody', views.save_melody, name="save-melody"),
    path('my_melodies', views.my_melodies, name="my-melodies"),
    path('get_melodies', views.get_melodies, name="get-melodies"),
    path('delete_melody', views.delete_melody, name="delete-melody"),
    path('add_vote', views.add_vote, name="add_vote"),
    path('melodies', views.melodies, name="melodies")
]
