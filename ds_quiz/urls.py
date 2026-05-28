from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 只要是進入主網址，就去載入 quiz.urls 的設定
    path('', include('quiz.urls')), 
]