from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from .models import find_user_by_reg, is_user_banned, check_password, has_taken_test

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        regno = request.form['regno']
        password = request.form['pw']
        test_code = request.form['code']

        # Check if the user exists
        user = find_user_by_reg(regno)
        if not user:
            flash("Register number not found.")
            return redirect(url_for('auth.login'))

        # Check password
        if not check_password(regno, password):
            flash("Incorrect password.")
            return redirect(url_for('auth.login'))

        # Check if the user is banned
        banned, ban_timer = is_user_banned(regno)
        if banned:
            flash(f"You are banned until {ban_timer}.")
            return redirect(url_for('auth.login'))

        # Check if the test code is valid
        question_set = current_app.mongo.db.question_sets.find_one({"code": test_code})
        if not question_set:
            flash("Invalid test code.")
            return redirect(url_for('auth.login'))

        # Check if the user has already taken the test
        if has_taken_test(regno, test_code):
            flash("You have already taken this test.")
            return redirect(url_for('auth.login'))

        # Set session variables and redirect to the test page
        session['regno'] = regno
        session['test_code'] = test_code
        session['test_in_progress'] = True

        return redirect(url_for('views.test', code=test_code))

    return render_template('login.html')
