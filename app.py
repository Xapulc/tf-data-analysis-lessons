import os

from utils import send_result_to_telegram, send_result_to_edu, get_variant


task_id = os.getenv("task_id")

if task_id == "12277":
    from stat_task1.test import max_score, salt, min_variant, max_variant, check_solution
    task_name = "Задание 1"
elif task_id == "12559":
    from stat_task2.test import max_score, salt, min_variant, max_variant, check_solution
    task_name = "Задание 2"
else:
    print(f"Некорректный номер задания: {task_id}")
    send_result_to_edu("Error", 0, 1)
    quit()


try:
    if task_name == "Задание 1":
        from student_work.task1.solution import chat_id
    elif task_name == "Задание 2":
        from student_work.task2.solution import chat_id
except Exception as e:
    print("Chat ID не указана")
    send_result_to_edu("Error", 0, max_score)
    quit()
    
try:
    if task_name == "Задание 1":
        from student_work.task1.solution import solution
    elif task_name == "Задание 2":
        from student_work.task2.solution import solution
except Exception as e:
    comment = f"Ошибка при импортах. Тип ошибки: {type(e)}, сообщение: {str(e)}"
    print(comment)
    send_result_to_telegram(chat_id, comment)
    send_result_to_edu("Error", 0, max_score)
    quit()
    
variant = get_variant(chat_id, salt, min_variant, max_variant)
check_solution_answer = check_solution(variant, solution)

task_score = check_solution_answer[0]
comment = check_solution_answer[1]
status = check_solution_answer[2]
attachment_list = check_solution_answer[3] if len(check_solution_answer) > 3 else None

print(comment)
send_result_to_telegram(chat_id, comment, attachment_list)
send_result_to_edu(status, task_score, max_score)
