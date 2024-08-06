from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app

views = Blueprint('views', __name__)

@views.route('/test/<code>', methods=['GET', 'POST'])
def test(code):
    if session.get('test_in_progress') is not True:
        flash("You cannot retake the test.")
        return redirect(url_for('auth.login'))

    regno = session.get('regno')

    # Fetch the question set from the database
    question_set = current_app.mongo.db.question_sets.find_one({"code": code})

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
        current_app.mongo.db.user.update_one(
            {"register_number": regno},
            {"$set": {f"completed_tests.{code}": score}}
        )

        # Clear the session progress
        session.pop('test_in_progress', None)

        flash(f"Test submitted successfully! Your score is {score:.2f}%.")
        return redirect(url_for('views.view_scores'))

    return render_template('test.html', questions=question_set['questions'])

@views.route('/rules', methods=['GET', 'POST'])
def rules():
    if request.method == 'POST':
        if 'test_in_progress' in session:
            return redirect(url_for('views.test', code=session['test_code']))
        else:
            return redirect(url_for('auth.login'))
    
    return render_template('rules.html')
