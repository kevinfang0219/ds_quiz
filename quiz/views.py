import random
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .models import Question, Choice, QuizRecord

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    error_message = None
    # 處理在首頁卡片直接登入的邏輯
    if request.method == 'POST' and request.POST.get('action') == 'login':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            error_message = "帳號或密碼錯誤，請重新確認。"
            
    # 如果使用者已登入，就去資料庫撈取他「最近 3 次」的作答紀錄 (這裡從 [:5] 改成了 [:3])
    user_records = []
    if request.user.is_authenticated:
        user_records = QuizRecord.objects.filter(user=request.user).order_by('-created_at')[:3]

    return render(request, 'quiz/home.html', {
        'error_message': error_message,
        'user_records': user_records
    })

@login_required
def start_quiz(request):
    num_questions = 5
    if request.method == 'POST':
        num_questions = int(request.POST.get('num_questions', 5))

    request.session['answers'] = {}
    request.session['start_time'] = timezone.now().timestamp()
    
    wrong_history = request.session.get('wrong_history', [])
    all_ids = list(Question.objects.exclude(id=69).values_list('id', flat=True))
    
    valid_wrong_ids = [qid for qid in wrong_history if qid in all_ids]
    random.shuffle(valid_wrong_ids)
    
    selected_ids = []
    
    for qid in valid_wrong_ids:
        if len(selected_ids) < num_questions:
            selected_ids.append(qid)
            
    remaining_ids = [qid for qid in all_ids if qid not in selected_ids]
    random.shuffle(remaining_ids)
    
    needed = num_questions - len(selected_ids)
    selected_ids.extend(remaining_ids[:needed])
    random.shuffle(selected_ids)
    
    request.session['question_ids'] = selected_ids
    return redirect('take_quiz', q_index=0)

@login_required
def take_quiz(request, q_index):
    question_ids = request.session.get('question_ids', [])
    total_questions = len(question_ids)

    if q_index >= total_questions or total_questions == 0:
        return redirect('quiz_result')

    current_q_id = question_ids[q_index]
    question = Question.objects.get(id=current_q_id)
    
    all_choices = list(question.choices.all())
    normal_choices = []
    last_choices = []
    
    fixed_keywords = ["以上皆是", "以上皆非", "以上皆對", "皆非"]
    
    for choice in all_choices:
        if any(keyword in choice.text for keyword in fixed_keywords):
            last_choices.append(choice)
        else:
            normal_choices.append(choice)
    
    session_key = request.session.session_key or 'default_key'
    random.seed(f"{session_key}_{question.id}")
    random.shuffle(normal_choices)
    random.seed()
    
    final_choices = normal_choices + last_choices
    
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
        'choices': final_choices,
        'q_index': q_index + 1,
        'total_questions': total_questions,
        'error_message': error_message,
        'show_feedback': show_feedback,
        'selected_choice_id': selected_choice_id,
    })

@login_required
def quiz_result(request):
    answers = request.session.get('answers', {})
    start_time = request.session.get('start_time')
    question_ids = request.session.get('question_ids', [])

    duration = 0
    if start_time:
        duration = int(timezone.now().timestamp() - start_time)

    wrong_questions_list = []
    wrong_details = []
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
            
            correct_choice = question.choices.filter(is_correct=True).first()
            wrong_details.append({
                'question': question,
                'user_choice': selected_choice,
                'correct_choice': correct_choice
            })

    current_wrong = request.session.get('wrong_history', [])
    for wid in wrong_ids:
        if wid not in current_wrong:
            current_wrong.append(wid)
    correct_ids = [int(qid) for qid in answers.keys() if int(qid) not in wrong_ids]
    current_wrong = [wid for wid in current_wrong if wid not in correct_ids]
    request.session['wrong_history'] = current_wrong

    total = len(question_ids)
    final_score = int((score / total) * 100) if total > 0 else 0

    try:
        record = QuizRecord.objects.create(user=request.user, duration_seconds=duration, score=final_score)
    except TypeError:
        record = QuizRecord.objects.create(duration_seconds=duration, score=final_score)
        
    record.wrong_questions.set(wrong_questions_list)

    return render(request, 'quiz/result.html', {
        'score': final_score,
        'duration': duration,
        'wrong_questions': wrong_questions_list,
        'wrong_details': wrong_details,
        'total': total,
        'correct_count': score
    })

@login_required
def leaderboard(request):
    top_records = QuizRecord.objects.exclude(user__isnull=True).order_by('-score', 'duration_seconds')[:10]
    return render(request, 'quiz/leaderboard.html', {
        'top_records': top_records
    })

@login_required
def record_detail(request, record_id):
    # 透過 ID 抓取紀錄，並加上 user=request.user 確保只能看「自己的」紀錄
    record = get_object_or_404(QuizRecord, id=record_id, user=request.user)
    
    # 撈出這筆紀錄中答錯的所有題目
    wrong_questions = record.wrong_questions.all()
    
    wrong_details = []
    for q in wrong_questions:
        correct_choice = q.choices.filter(is_correct=True).first()
        wrong_details.append({
            'question': q,
            'correct_choice': correct_choice
        })
        
    return render(request, 'quiz/record_detail.html', {
        'record': record,
        'wrong_details': wrong_details
    })