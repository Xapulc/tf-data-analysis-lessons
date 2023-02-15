from var0.test import test as var0_test
from var1.test import test as var1_test


max_score = 6

def check_solution(variant, solution):
    test = None
    if variant == 0:
        test = var0_test
    elif variant == 1:
        test = var1_test
    else:
        return 0, f"Вариант {variant} не найден", "Error"
    
    try:
        task_score = test(solution)
    except Exception as e:
        return 0, f"Ошибка в решающей функции. Тип ошибки: {type(e)}, сообщение ошибки: {str(e)}", "Error"
   
    return task_score, f"Количество набранных баллов = {task_score}", "Done"
except Exception as e:
    write_task_res(f"Exception in solution function. Type: {type(e)}, messange: {str(e)}", 0)
else:
    write_task_res("Done", task_score)
