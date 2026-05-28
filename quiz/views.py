import random  # 新增的隨機模組
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Question, Choice, QuizRecord

def home(request):
    return render(request, 'quiz/home.html')

def start_quiz(request):
    request.session['answers'] = {}
    request.session['start_time'] = timezone.now().timestamp()
    
    # 取得所有題目的 ID
    all_ids = list(Question.objects.values_list('id', flat=True))
    
    # 將題目順序隨機打亂
    random.shuffle(all_ids)
    
    # 取出前 15 題的 ID，存入 session 中，這樣這回合的題目就固定下來了
    request.session['question_ids'] = all_ids[:15]

    return redirect('take_quiz', q_index=0)

def take_quiz(request, q_index):
    # 從 session 讀取這回合隨機抽出的 15 題
    question_ids = request.session.get('question_ids', [])
    total_questions = len(question_ids)

    # 如果已經超過題數，跳轉到結算畫面
    if q_index >= total_questions or total_questions == 0:
        return redirect('quiz_result')

    # 用目前的題號 (q_index) 從 ID 列表中抓出真正的題目
    current_q_id = question_ids[q_index]
    question = Question.objects.get(id=current_q_id)
    
    selected_choice_id = None
    show_feedback = False
    error_message = None

    if request.method == 'POST':
        if 'btn_next' in request.POST:
            return redirect('take_quiz', q_index=q_index + 1)

        selected_choice_id = request.POST.get('choice')
        if selected_choice_id:
            selected_choice_id = int(selected_choice_id)
            answers = request.session.get('answers', {})
            answers[str(question.id)] = str(selected_choice_id)
            request.session['answers'] = answers
            show_feedback = True
        else:
            error_message = "請至少選擇一個選項喔！"

    return render(request, 'quiz/question.html', {
        'question': question,
        'q_index': q_index + 1,
        'total_questions': total_questions,
        'error_message': error_message,
        'show_feedback': show_feedback,
        'selected_choice_id': selected_choice_id,
    })

def quiz_result(request):
    answers = request.session.get('answers', {})
    start_time = request.session.get('start_time')
    question_ids = request.session.get('question_ids', [])

    duration = 0
    if start_time:
        duration = int(timezone.now().timestamp() - start_time)

    wrong_questions_list = []
    score = 0

    # 核對答案
    for q_id_str, choice_id_str in answers.items():
        question = Question.objects.get(id=int(q_id_str))
        selected_choice = Choice.objects.get(id=int(choice_id_str))
        
        if selected_choice.is_correct:
            score += 1
        else:
            wrong_questions_list.append(question)

    # 儲存這筆測驗紀錄到資料庫
    record = QuizRecord.objects.create(duration_seconds=duration)
    record.wrong_questions.set(wrong_questions_list)

    # 用這回合實際測驗的題數 (也就是 15) 來計算分數
    total = len(question_ids)
    final_score = int((score / total) * 100) if total > 0 else 0

    return render(request, 'quiz/result.html', {
        'score': final_score,
        'duration': duration,
        'wrong_questions': wrong_questions_list,
        'total': total,
        'correct_count': score
    })