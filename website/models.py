from bson.objectid import ObjectId
from datetime import datetime, timedelta
from . import mongo
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

def add_user(register_number, password):
    hashed_password = generate_password_hash(password)
    user_data={
        "register_number":register_number,
        "password": hashed_password,
        "banned":False,
        "ban_timer":None,
        "completed_tests":{}
    }
    current_app.mongo.db.user.insert_one(user_data)

def find_user_by_reg(register_number):
    return current_app.mongo.db.user.find_one({"register_number":register_number})

def ban_user(user_id, duration_minutes=5):
    ban_until = datetime.now() + timedelta(minutes=duration_minutes)
    current_app.mongo.db.user.update_one(
        {"_id":ObjectId(user_id)},
        {"$set": {"banned":True, "ban_timer":ban_until}})
    
def is_user_banned(register_number):
    user=find_user_by_reg(register_number)
    if user:
        if user["banned"]:
            if user["ban_timer"] and datetime.now()>user["ban_timer"]:
                current_app.mongo.db.user.update_one(
                    {"register_number": register_number}, 
                    {"$set": {"banned":False, "ban_timer": None}}
                )
                return False
            return True, user["ban_timer"]
    return False, None

def record_test_completion(register_number, question_set_code, score, correct_answers):
    current_app.mongo.db.user.update_one(
        {"register_number": register_number},
        {"$set": {f"completed_tests.{question_set_code}": {"score": score, "correct_answers": correct_answers}}}
    )

def has_taken_test(register_number, question_set_code):
    user = find_user_by_reg(register_number)
    if user:
        return user.get("completed_tests", {}).get(question_set_code, False)
    return False

def check_password(register_number, password):
    user = find_user_by_reg(register_number)
    if user:
        return check_password_hash(user["password"], password)
    return False