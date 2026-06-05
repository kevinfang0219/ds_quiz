from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('start/', views.start_quiz, name='start_quiz'),
    path('take/<int:q_index>/', views.take_quiz, name='take_quiz'),
    path('result/', views.quiz_result, name='quiz_result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]