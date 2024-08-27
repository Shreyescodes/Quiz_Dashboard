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
            
            # Debugging print statement
            print(quiz_data)  # Check the structure of quiz_data

            return redirect('quiz:quiz_types')
    else:
        form = UploadFileForm()
    return render(request, 'quiz/upload.html', {'form': form})

def quiz_types(request):
    types = set((row.get('T_ID'), row.get('Type')) for row in quiz_data)
    return render(request, 'quiz/quiz_types.html', {'types': types})

def display_quiz(request, t_id, quiz_type):
    print("Rendering quiz.html")
    questions = [row for row in quiz_data if row['T_ID'] == t_id and row['Type'] == quiz_type]

    if request.method == 'POST':
        score = 0
        total_credits = 0
        earned_credits = 0

        for question in questions:
            total_credits += int(question.get('Credits', 0))  #total credits for all questions
            selected_answer = request.POST.get(question['Questions'])
            if selected_answer == question['Correct answer']:
                score += 1
                earned_credits += int(question.get('Credits', 0))  #credits for correctly answered questions

        # Calculate the percentage of credits earned
        percentage = (earned_credits / total_credits) * 100 if total_credits > 0 else 0

        return render(request, 'quiz/score.html', {
            'score': score,
            'total': len(questions),
            'percentage': percentage,
            'incorrect_questions': [(question['Questions'], question['Correct answer'])
                                    for question in questions
                                    if request.POST.get(question['Questions']) != question['Correct answer']]
        })
        return render(request, 'quiz/score.html', {'score': score, 'total': total_questions})

    return render(request, 'quiz/quiz.html', {'questions': questions})

def quiz_detail(request, question_type):
    # Retrieve all questions for the selected quiz type
    questions = QuizQuestion.objects.filter(question_type=question_type)
    return render(request, 'quiz/quiz.html', {'questions': questions, 'quiz_type': question_type})

def quiz_types(request):
    types = [
        (1, 'Python'),
        (2, 'Java'),
        (3, 'JavaScript')

    ]
    return render(request, 'quiz/quiz_types.html', {'types': types})