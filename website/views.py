from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from .models import record_test_completion

views = Blueprint('views', __name__)

@views.route('/test/<code>', methods=['GET', 'POST'])
def test(code):
    if 'regno' not in session or 'test_code' not in session:
        flash('User not logged in.', 'error')
        return redirect(url_for('auth.login'))

    if session.get('test_in_progress') is not True:
        flash("You cannot retake the test.")
        return redirect(url_for('auth.login'))

    regno = session.get('regno')

    # Fetch the question set from the database
    question_set = current_app.mongo.db.question_sets.find_one({"code": code})
    
    if not question_set:
        flash("Invalid test code. Please try again.", "error")
        return redirect(url_for('auth.login'))
    
    question_dict = {question['question']:question['options'] for question in question_set['questions']}

    if request.method == 'POST':
        # Process user's answers
        answers = request.form.to_dict()
        correct_answers = 0

        for question in question_set['questions']:
            question_id = question['question']
            selected_answer = answers.get(question_id)
            if selected_answer == question['answer']:
                correct_answers += 1

        score = correct_answers / len(question_set['questions']) * 100

        # Record test completion and score
        record_test_completion(regno, code,score,correct_answers)

        # Clear the session progress
        session.pop('test_in_progress', None)

        flash(f"Test submitted successfully!")
        return redirect(url_for('views.score',code=code))

    return render_template('test.html', question_dict=question_dict, code=code, regno=regno)

@views.route('/rules', methods=['GET', 'POST'])
def rules():
    if 'regno' not in session or 'test_code' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('auth.login'))


    if request.method == 'POST':
        if 'test_in_progress' in session:
            return redirect(url_for('views.test', code=session['test_code']))
        else:
            return redirect(url_for('auth.login'))
    
    return render_template('rules.html')

@views.route('/score/<code>')
def score(code):
    if 'regno' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('auth.login'))
    
    regno = session.get('regno')
    question_set = current_app.mongo.db.question_sets.find_one({"code": code})
    question_dict = {question['question']:question['options'] for question in question_set['questions']}
    

    user = current_app.mongo.db.user.find_one({"register_number": regno})
    completed_test = user["completed_tests"].get(code)

    if not completed_test:
        print("test results not found.",'info')#debugging statement, remove later
        return redirect(url_for('auth.login'))

    score = completed_test['score']
    correct_answers = completed_test['correct_answers']

    return render_template('score.html',code=code,score=score, correct_answers=correct_answers,noQ=str(len(question_dict)),regno=regno)

@views.route('/deny', methods=['POST'])
def deny():
    flash('You have declined the exam rules.', 'warning')
    session.pop('regno', None)
    session.pop('test_code', None)
    return redirect(url_for('auth.login'))