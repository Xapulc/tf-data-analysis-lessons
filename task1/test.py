import os
import pandas as pd 
import numpy as np
import email as em
import smtplib

from var0.test import test as var0_test
from var1.test import test as var1_test
from var2.test import test as var2_test
from var3.test import test as var3_test
from .utils import send_result


def write_task_res(status, task_score, to_email):
    env_file = os.getenv("GITHUB_ENV")
    max_score = 4
    answer = f"status={status}\nmax_score={max_score}\ntask_score={task_score}\n"
    send_result(to_email, "task1", answer)
    print(answer)
    with open(env_file, "a") as myfile:
        myfile.write(answer)

        
try:
    from student_work.task1.solution import variant, solution, email as to_email
except Exception as e:
    write_task_res(f"Exception in imports. Type: {type(e)}, messange: {str(e)}", 0, to_email) # TODO: fix to_email??
    quit()


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
    write_task_res(f"Variant {variant} not found", 0, to_email)
    quit()

try:
    task_score = test(solution)
except Exception as e:
    write_task_res(f"Exception in solution function. Type: {type(e)}, messange: {str(e)}", 0, to_email)
else:
    write_task_res("Done", task_score, to_email)
