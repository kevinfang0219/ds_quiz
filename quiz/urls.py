from django.urls import path
from . import views

urlpatterns = [
    # 1. 這是新的！讓首頁顯示封面
    path('', views.home, name='home'),
    
    # 2. 修改這裡！把原本的開始測驗網址，加上 'start/'
    path('start/', views.start_quiz, name='start_quiz'),
    
    # 3. 下面兩個維持不變
    path('question/<int:q_index>/', views.take_quiz, name='take_quiz'),
    path('result/', views.quiz_result, name='quiz_result'),
]