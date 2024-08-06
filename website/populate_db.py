import sys
import os
from flask import current_app
from website import create_app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from website.models import add_user

app = create_app()

registration_numbers = [
    {"register_number": "222BCAA49", "password": "password1"},
    {"register_number": "222BCAA50", "password": "password2"},
]

question_sets = [
    {"code": "SET1", "questions": [
        {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
        {"question": "What is 3 + 3?", "options": ["6", "7", "3", "9"], "answer": "6"},
    ]},
    {"code": "SET2", "questions": [
        {"question": "What is 4 + 4?", "options": ["6", "7", "8", "9"], "answer": "8"}
    ]},
]

with app.app_context():

    for user in registration_numbers:
        add_user(user["register_number"], user["password"])

    for question_set in question_sets:
        current_app.mongo.db.question_sets.insert_one(question_set)

    print("Data has been inserted successfully!")