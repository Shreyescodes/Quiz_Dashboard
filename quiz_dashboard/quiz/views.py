import random
import csv
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.contrib import messages

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
    global quiz_data

    # Retrieve the quiz questions based on T_ID and Type
    questions = []
    options = []
    correct_options = []

    for row in quiz_data:
        if row['T_ID'] == t_id and row['Type'] == quiz_type:
            questions.append(row['Questions'])
            options.append([row['Option1'], row['Option2'], row['Option3'], row['Option4']])
            correct_options.append(row['Correct answer'])

    # Check if there are any questions for the quiz type and T_ID
    if not questions:
        return render(request, 'quiz/no_questions.html')

    # Reset the quiz if the session data is inconsistent
    if ('shuffled_indices' not in request.session or
        len(request.session['shuffled_indices']) != len(questions) or
        request.session.get('question_index', 0) >= len(questions)):
        request.session['shuffled_indices'] = list(range(len(questions)))
        random.shuffle(request.session['shuffled_indices'])
        request.session['question_index'] = 0
        request.session['score'] = 0
        request.session['incorrect_questions'] = []

    shuffled_indices = request.session['shuffled_indices']
    question_index = request.session['question_index']

    # Check if it's the last question
    is_last_question = (question_index == len(questions) - 1)

    if request.method == 'POST':
        # Handle answer submission
        selected_answer = request.POST.get('answer')

        if not selected_answer:
            messages.error(request, "Please select an option before proceeding.")
        else:
            current_question_index = shuffled_indices[question_index]
            if selected_answer == correct_options[current_question_index]:
                request.session['score'] = request.session.get('score', 0) + 1
            else:
                incorrect_questions = request.session.get('incorrect_questions', [])
                incorrect_questions.append({
                    'question': questions[current_question_index],
                    'correct_answer': correct_options[current_question_index],
                    'user_answer': selected_answer
                })
                request.session['incorrect_questions'] = incorrect_questions

            if not is_last_question:
                request.session['question_index'] = question_index + 1
            else:
                # Show the score
                score = request.session.get('score', 0)
                total_questions = len(questions)
                percentage = (score / total_questions) * 100 if total_questions > 0 else 0

                incorrect_questions = request.session.get('incorrect_questions', [])

                # Clear session variables
                for key in ['score', 'question_index', 'incorrect_questions', 'shuffled_indices']:
                    request.session.pop(key, None)

                return render(request, 'quiz/score.html', {
                    'score': score,
                    'total': total_questions,
                    'percentage': percentage,
                    'incorrect_questions': incorrect_questions
                })

            return redirect('quiz:display_quiz', t_id=t_id, quiz_type=quiz_type)

    # Render the current question
    current_question_index = shuffled_indices[question_index]
    
    return render(request, 'quiz/quiz.html', {
        'question': f"{question_index + 1}. {questions[current_question_index]}",
        'options': options[current_question_index],
        'is_last_question': is_last_question,
        'total_questions': len(questions),
        'current_question_number': question_index + 1,
        'quiz_type': quiz_type,
    })
    
def quiz_detail(request, question_type):
    questions = QuizQuestion.objects.filter(question_type=question_type)
    return render(request, 'quiz/quiz.html', {'questions': questions, 'quiz_type': question_type})

def quiz_types(request):
    types = [
        (1, 'Python'),
        (2, 'Java'),
        (3, 'Javascript')
        # Add other types as needed
    ]
    return render(request, 'quiz/quiz_types.html', {'types': types})
