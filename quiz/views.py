import random
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Question, Choice, QuizRecord

def home(request):
    return render(request, 'quiz/home.html')

def start_quiz(request):
    # 接收首頁傳來的題數設定 (預設 5 題)
    num_questions = 5
    if request.method == 'POST':
        num_questions = int(request.POST.get('num_questions', 5))

    request.session['answers'] = {}
    request.session['start_time'] = timezone.now().timestamp()
    
    # 讀取使用者的「歷史錯題本」
    wrong_history = request.session.get('wrong_history', [])
    
    # 取得所有題目的 ID
    all_ids = list(Question.objects.exclude(id=69).values_list('id', flat=True))
    
    # 篩選出有效的歷史錯題
    valid_wrong_ids = [qid for qid in wrong_history if qid in all_ids]
    random.shuffle(valid_wrong_ids)
    
    selected_ids = []
    
    # 優先把錯題塞進這次的考卷中
    for qid in valid_wrong_ids:
        if len(selected_ids) < num_questions:
            selected_ids.append(qid)
            
    # 如果錯題不夠，剩下的用隨機題目補滿
    remaining_ids = [qid for qid in all_ids if qid not in selected_ids]
    random.shuffle(remaining_ids)
    
    needed = num_questions - len(selected_ids)
    selected_ids.extend(remaining_ids[:needed])
    
    # 再次打亂，讓學生不會一開始就猜到前面都是錯題
    random.shuffle(selected_ids)
    
    request.session['question_ids'] = selected_ids

    return redirect('take_quiz', q_index=0)

def take_quiz(request, q_index):
    question_ids = request.session.get('question_ids', [])
    total_questions = len(question_ids)

    if q_index >= total_questions or total_questions == 0:
        return redirect('quiz_result')

    current_q_id = question_ids[q_index]
    question = Question.objects.get(id=current_q_id)
    
    # 選項隨機打亂邏輯：綁定 session key 與題號，確保送出表單後選項不會亂跳
    choices = list(question.choices.all())
    session_key = request.session.session_key or 'default_key'
    random.seed(f"{session_key}_{question.id}")
    random.shuffle(choices)
    random.seed() # 重置隨機狀態
    
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
        'choices': choices,  # 將打亂後的選項傳給前端
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
    wrong_ids = []
    score = 0

    for q_id_str, choice_id_str in answers.items():
        question = Question.objects.get(id=int(q_id_str))
        selected_choice = Choice.objects.get(id=int(choice_id_str))
        
        if selected_choice.is_correct:
            score += 1
        else:
            wrong_questions_list.append(question)
            wrong_ids.append(question.id)

    # 錯題本 (間隔學習) 更新邏輯
    current_wrong = request.session.get('wrong_history', [])
    # 1. 這次答錯的，加進錯題本
    for wid in wrong_ids:
        if wid not in current_wrong:
            current_wrong.append(wid)
    # 2. 這次答對的，從錯題本裡移除（代表學會了）
    correct_ids = [int(qid) for qid in answers.keys() if int(qid) not in wrong_ids]
    current_wrong = [wid for wid in current_wrong if wid not in correct_ids]
    request.session['wrong_history'] = current_wrong

    record = QuizRecord.objects.create(duration_seconds=duration)
    record.wrong_questions.set(wrong_questions_list)

    total = len(question_ids)
    final_score = int((score / total) * 100) if total > 0 else 0

    return render(request, 'quiz/result.html', {
        'score': final_score,
        'duration': duration,
        'wrong_questions': wrong_questions_list,
        'total': total,
        'correct_count': score
    })