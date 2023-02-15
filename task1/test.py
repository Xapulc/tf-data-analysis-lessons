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
        task_score = test(solution)
    except Exception as e:
        return 0, f"Ошибка в решающей функции. Тип ошибки: {type(e)}, сообщение ошибки: {str(e)}", "Error"
   
    return task_score, f"Количество набранных баллов = {task_score}", "Done"
