from .var0.test import test as var0_test
from .var1.test import test as var1_test
from .var2.test import test as var2_test
from .var3.test import test as var3_test


max_score = 4

def check_solution(variant, solution):
    test = None
    if variant == 0:
        test = var0_test
    elif variant == 1:
        test = var1_test
    elif variant == 2:
        test = var2_test
    elif variant == 3:
        test = var3_test
    else:
        return 0, f"Вариант {variant} не найден", "Error"
    
    try:
        score_list = test(solution)
    except Exception as e:
        return 0, f"Ошибка в решающей функции. Тип ошибки: {type(e)}, сообщение ошибки: {str(e)}", "Error"
    
    message = f"В задании 1 у вас *{variant}-й вариант*.\n"
    task_score = 0
    
    for score_element in score_list:
        score = 1 if score_element["test_error"] < score_element["max_error"] else 0
        task_score += score
        message += f"На выборках размера `{score_element['sample_size']}` " \
                   + f"ваша средняя ошибка равна `{score_element['test_error']}` " \
                   + f"при пороге `{score_element['max_error']}`. " \
                   + f"За этот пункт вы получаете количество баллов = {score}.\n"
        
    message += f"Ваш общий результат: *{task_score} из {max_score}*."
   
    return task_score, message, "Done"
