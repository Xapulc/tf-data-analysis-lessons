import os

from task1 import test as test1
from task2 import test as test2

from student_work.solution import variant, solution, email as to_email # Обработать исключения

task_id = os.getenv("task_id")
subject = None

if task_id == "12277":
    task_score, max_score, comment = test1(variant, solution)
    subject = f"""Экзамен "Математическая статистика", задание 1"""
elif task_id == "12559":
    task_score, max_score, comment = test2(variant, solution)
    subject = f"""Экзамен "Математическая статистика", задание 2"""

send_result(to_email, subject, comment)
