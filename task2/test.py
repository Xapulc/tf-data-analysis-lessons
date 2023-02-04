import os
import pandas as pd 
import numpy as np

from var0.test import test as var0_test
from var1.test import test as var1_test


def write_task_res(status, task_score):
    env_file = os.getenv("GITHUB_ENV")
    max_score = 6
    answer = f"status={status}\nmax_score={max_score}\ntask_score={task_score}\n"
    print(answer)
    with open(env_file, "a") as myfile:
        myfile.write(answer)

        
try:
    from student_work.task2.solution import variant, solution
except Exception as e:
    write_task_res(f"Exception in imports. Type: {type(e)}, messange: {str(e)}", 0)
    quit()


test = None
if variant == 0:
    test = var0_test
elif variant == 1:
    test = var1_test
else:
    write_task_res(f"Variant {variant} not found", 0)
    quit()

try:
    task_score = test(solution)
except Exception as e:
    write_task_res(f"Exception in solution function. Type: {type(e)}, messange: {str(e)}", 0)
else:
    write_task_res("Done", task_score)
