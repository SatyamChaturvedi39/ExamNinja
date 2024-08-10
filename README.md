# ExamNinja: Exam Proctoring System
ExamNinja is a web-based exam proctoring system designed to ensure academic integrity during online tests. Built with pure HTML,CSS,JS for frontend, Flask as the backend framework and MongoDB as the database, the system provides a secure environment for students to complete exams.

Features:

1.)User Authentication: Students log in using a unique registration number, ensuring that only authorized users can access the exam.

2.)Exam Management: Each exam is associated with a specific test code. Students can only take the test once, and their progress is tracked through sessions.

3.)Question Handling: Questions are stored in MongoDB, and the system dynamically fetches and displays them during the exam. The questions are presented with multiple-choice options, and the user's selected answers are processed and scored.

4.)Security Measures: The system enforces strict exam rules, including restrictions on tab switching, right-clicking, and keyboard shortcuts. A timer is also included to automatically submit the exam after a set time.

5.)Post-Exam Feedback: After submitting the exam, students receive their score in percentage along with the number of correct answers out of 10.

6.)Ban Feature: Users can be temporarily banned from taking exams based on specific conditions in the javascript.

7.)Session Management: If a user attempts to go back after logging in, they are automatically logged out or the history is deleted so that they cannot access the said page again to maintain the integrity of the test session.

The project demonstrates key concepts in web development, such as session management, database operations, and the integration of front-end and back-end technologies to create a seamless and secure online exam experience.
