import os

from utils import send_result_to_email, send_result_to_edu

task_id = os.getenv("task_id")

if task_id == "12277":
    from task1.test import max_score, check_solution
    task_name = "Задание 1"
elif task_id == "12559":
    from task2.test import max_score, check_solution
    task_name = "Задание 2"
else:
    print(f"Некорректный номер задания: {task_id}")
    
subject = 'Экзамен "Математическая статистика", ' + task_name


try:
    from student_work.solution import email as to_email
except Exception as e:
    send_result_to_edu("Error", 0, max_score)
    
try:
    from student_work.solution import variant, solution
except Exception as e:
    send_result_to_email(to_email, 
                         subject,
                         f"Ошибка при импортах. Тип ошибки: {type(e)}, сообщение: {str(e)}")
    send_result_to_edu("Error", 0, max_score)
    
    
task_score, max_score, comment, status = check_solution(variant, solution)

send_result_to_email(to_email, subject, comment)
send_result_to_edu(status, task_score, max_score)
