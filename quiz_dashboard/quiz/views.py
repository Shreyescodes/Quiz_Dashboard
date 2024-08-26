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


# def display_quiz(request, t_id, quiz_type):
#     print("Rendering quiz.html")
#     questions = [row for row in quiz_data if row['T_ID'] == t_id and row['Type'] == quiz_type]

#     if request.method == 'POST':
#         score = 0
#         for question in questions:
#             selected_answer = request.POST.get(question['Questions']).strip() if request.POST.get(question['Questions']) else None
#             correct_answer = question['Correct answer'].strip()
            
#             print(f"Question: {question['Questions']}, Selected Answer: {selected_answer}, Correct Answer: {correct_answer}")  # Debugging print statement

#             # Compare selected answer with correct answer
#             if selected_answer and selected_answer == correct_answer:
#                 score += 1

#         # Render the score template after quiz completion
#         return render(request, 'quiz/score.html', {'score': score, 'total': len(questions)})
    
#     # Render the quiz template
#     return render(request, 'quiz/quiz.html', {'questions': questions, 'quiz_type': quiz_type})

def display_quiz(request, t_id, quiz_type):
    print("Rendering quiz.html")
    # Filter the questions based on T_ID and Type
    questions = [row for row in quiz_data if row['T_ID'] == t_id and row['Type'] == quiz_type]

    if request.method == 'POST':
        score = 0
        total_questions = len(questions)

        for question in questions:
            # Get the user's selected answer for each question
            selected_answer = request.POST.get(question['Questions'])
            correct_answer = question['Correct answer']

            # Print debugging information
            print(f"Question: {question['Questions']}")
            print(f"Selected Answer: {selected_answer}")
            print(f"Correct Answer: {correct_answer}")

            # Handle if no answer was selected (skip unanswered questions)
            if selected_answer is not None:
                # Compare selected answer with correct answer
                if selected_answer.strip().lower() == correct_answer.strip().lower():
                    score += 1

        # Print the final score for debugging
        print(f"Final Score: {score}/{total_questions}")

        # Render the score template after quiz completion
        return render(request, 'quiz/score.html', {'score': score, 'total': total_questions})

    # Render the quiz template
    return render(request, 'quiz/quiz.html', {'questions': questions, 'quiz_type': quiz_type})

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




