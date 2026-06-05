from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    # 定義難易度選項
    DIFFICULTY_CHOICES = [
        ('易', '易 (Easy)'),
        ('中', '中 (Medium)'),
        ('難', '難 (Hard)'),
    ]
    
    text = models.CharField("題目內容", max_length=500)
    # 新增這行難易度欄位，預設為「中」
    difficulty = models.CharField("難易度", max_length=1, choices=DIFFICULTY_CHOICES, default='中')
    
    def __str__(self):
        return f"[{self.difficulty}] {self.text}" # 順便讓後台標題顯示難易度，會比較好管理！

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name="所屬題目")
    text = models.CharField("選項內容", max_length=200)
    is_correct = models.BooleanField("是否為正確答案", default=False)

    def __str__(self):
        return self.text

class QuizRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    duration_seconds = models.IntegerField("作答時間(秒)")
    score = models.IntegerField("分數", default=0)
    wrong_questions = models.ManyToManyField(Question, blank=True, verbose_name="答錯的題目")
    created_at = models.DateTimeField("測驗時間", auto_now_add=True)

    def __str__(self):
        return f"測驗紀錄 ({self.created_at.strftime('%Y-%m-%d %H:%M')}) - 花費 {self.duration_seconds} 秒"