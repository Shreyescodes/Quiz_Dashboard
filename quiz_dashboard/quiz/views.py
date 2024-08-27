import csv
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import QuizQuestion

# Global variable to hold quiz data
quiz_data = []

def upload_file(request):
    global quiz_data
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            quiz_data = list(reader)
            return redirect('quiz:quiz_types')
    else:
        form = UploadFileForm()
    return render(request, 'quiz/upload.html', {'form': form})

def quiz_types(request):
    types = set((row.get('T_ID'), row.get('Type')) for row in quiz_data)
    return render(request, 'quiz/quiz_types.html', {'types': types})

def display_quiz(request, t_id, quiz_type):
    questions = [row for row in quiz_data if row['T_ID'] == t_id and row['Type'] == quiz_type]
    
    # Track the current question index
    question_index = request.session.get('question_index', 0)

    # Check if it's the last question
    is_last_question = (question_index == len(questions) - 1)

    if request.method == 'POST':
        # Handle answer submission
        selected_answer = request.POST.get(questions[question_index]['Questions'])
        if selected_answer == questions[question_index]['Correct answer']:
            score = request.session.get('score', 0)
            score += 1
            request.session['score'] = score

        # If not the last question, increment the question index
        if not is_last_question:
            question_index += 1
            request.session['question_index'] = question_index
            return redirect('quiz:display_quiz', t_id=t_id, quiz_type=quiz_type)

        # If last question, show the score
        score = request.session.get('score', 0)
        total_credits = sum(int(question.get('Credits', 0)) for question in questions)
        earned_credits = score * int(questions[0].get('Credits', 0))  # Credits per correct answer
        percentage = (earned_credits / total_credits) * 100 if total_credits > 0 else 0

        # Clear the session variables
        request.session['score'] = 0
        request.session['question_index'] = 0

        return render(request, 'quiz/score.html', {
            'score': score,
            'total': len(questions),
            'percentage': percentage,
            'incorrect_questions': [(question['Questions'], question['Correct answer'])
                                    for question in questions
                                    if request.POST.get(question['Questions']) != question['Correct answer']]
        })

    return render(request, 'quiz/quiz.html', {
        'question': questions[question_index],
        'is_last_question': is_last_question,
    })


def quiz_detail(request, question_type):
    # Retrieve all questions for the selected quiz type
    questions = QuizQuestion.objects.filter(question_type=question_type)
    return render(request, 'quiz/quiz.html', {'questions': questions, 'quiz_type': question_type})

# def quiz_types(request):
#     types = [
#         (1, 'Python'),
#         (2, 'Java'),
#         (3, 'JavaScript')
#         # Add other types as needed
#     ]
#     return render(request, 'quiz/quiz_types.html', {'types': types})