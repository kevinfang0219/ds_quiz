from django.db import models

class Question(models.Model):
    text = models.CharField("題目內容", max_length=500)
    
    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name="所屬題目")
    text = models.CharField("選項內容", max_length=200)
    is_correct = models.BooleanField("是否為正確答案", default=False)

    def __str__(self):
        return self.text

class QuizRecord(models.Model):
    duration_seconds = models.IntegerField("作答時間(秒)")
    wrong_questions = models.ManyToManyField(Question, blank=True, verbose_name="答錯的題目")
    created_at = models.DateTimeField("測驗時間", auto_now_add=True)

    def __str__(self):
        return f"測驗紀錄 ({self.created_at.strftime('%Y-%m-%d %H:%M')}) - 花費 {self.duration_seconds} 秒"