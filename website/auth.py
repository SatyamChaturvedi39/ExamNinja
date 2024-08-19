from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from .models import find_user_by_reg, is_user_banned, check_password, has_taken_test,ban_user
from datetime import datetime

auth = Blueprint('auth', __name__)
teachers=["222MCS01", "222TR01"]
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        regno = request.form['regno']
        password = request.form['pw']
        test_code = str(request.form['code'])
        if regno in teachers:
            return redirect(url_for('views.invi', code=session['test_code']))
        user = find_user_by_reg(regno)
        if not user:
            flash("Register number not found.",'error')
            return redirect(url_for('auth.login'))

        if not check_password(regno, password):
            flash("Incorrect password.",'error')
            return redirect(url_for('auth.login'))

        [banned, ban_timer] = is_user_banned(regno)
        if banned:
            bantime=ban_timer.strftime('%I:%M %p')
            flash(f"You are banned until {bantime}.",'warning')
            return redirect(url_for('auth.login'))

        question_set = current_app.mongo.db.question_sets.find_one({"code": test_code})
        if not question_set:
            flash("Invalid test code.",'error')
            return redirect(url_for('auth.login'))

        if has_taken_test(regno, test_code):
            flash("You have already taken this test.",'warning')
            return redirect(url_for('auth.login'))

        session['regno'] = regno
        session['test_code'] = test_code
        session['test_in_progress'] = True

        return redirect(url_for('views.rules'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/ban/<regno>',methods=['GET'])
def ban(regno):
    if 'regno' not in session:
        flash('You need to log in first.','error')
        return redirect(url_for('auth.login'))
    
    user = find_user_by_reg(regno)
    if not user:
        flash('User not found.','error')
        return redirect(url_for('auth.login'))
    
    ban_user(regno)

    flash(f'The user {regno} has been banned.','warning')
    return redirect(url_for('auth.login'))