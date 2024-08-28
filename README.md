# Quiz Dashboard

A dynamic quiz dashboard application built using Python and Django. This application allows users to upload quiz questions via a CSV file, attempt the quiz, and view their score along with incorrectly answered questions.

## Features

- **CSV Upload**: Upload quiz questions from a CSV file.
- **Quiz Navigation**: Navigate between questions, highlighting the current question.
- **Score Calculation**: Calculate scores based on the correct answers.
- **Incorrect Questions**: Display the incorrectly answered questions and the correct answers.
- **Responsive UI**: User-friendly and responsive interface with a scrollable question navigation bar.
- **Dynamic Quiz Types**: Supports quiz categories such as Python, Java, and JavaScript.

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS
- **Data Handling**: CSV Parsing

## Installation

### Prerequisites

- Python 3.x
- Django 5.x

### Setup

1. Clone the repository:

```bash
   git clone https://github.com/Shreyescodes/quiz-dashboard.git
   cd quiz-dashboard
```

2. Create a virtual environment:
   Windows
```bash
.\env\Scripts\activate
```
MacOS/Linux

3. Activate the virtual environment:

On Windows:
```bash
source env/bin/activate
```

On macOS/Linux :
```bash
source env/bin/activate
```

4. Install the required dependencies:
```bash
   pip install -r requirements.txt
```

5. Apply migrations:

```bash
python manage.py migrate
```

6. Run the development server:

```bash
python manage.py runserver
```

Open your browser and navigate to http://127.0.0.1:8000.

Usage:

Upload Quiz Questions: Navigate to the upload page and upload a CSV file containing your quiz questions.
Select Quiz Type: Choose from the available quiz types.
Attempt the Quiz: Navigate through the questions, and your progress will be displayed at the top.
View Your Score: Once you've completed the quiz, view your score along with the incorrectly answered questions.

Contributing:

Contributions are welcome! Please feel free to submit a Pull Request.

License:

This project is licensed under the MIT License - see the LICENSE file for details.
