from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('voice-interact/', views.voice_interact, name='voice_interact'),
]
