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
    send_result_to_edu("Error", 0, 1)
    quit()
    
subject = 'Экзамен "Математическая статистика", ' + task_name


try:
    if task_name == "Задание 1":
        from student_work.task1.solution import email as to_email
    elif task_name == "Задание 2":
        from student_work.task2.solution import email as to_email
except Exception as e:
    print("Почта не указана")
    send_result_to_edu("Error", 0, max_score)
    quit()
    
try:
    if task_name == "Задание 1":
        from student_work.task1.solution import variant, solution
    elif task_name == "Задание 2":
        from student_work.task2.solution import variant, solution
except Exception as e:
    comment = f"Ошибка при импортах. Тип ошибки: {type(e)}, сообщение: {str(e)}"
    print(comment)
    send_result_to_email(to_email, subject, comment)
    send_result_to_edu("Error", 0, max_score)
    quit()
    
    
task_score, comment, status = check_solution(variant, solution)

print(comment)
send_result_to_email(to_email, subject, comment)
send_result_to_edu(status, task_score, max_score)
