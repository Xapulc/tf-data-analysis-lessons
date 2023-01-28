import os
import pandas as pd 
import numpy as np

from var1.test import test as var1_test

from student_work.task1 import variant
from student_work.task1 import decision


def write_task_res(status, task_score):
    env_file = os.getenv("GITHUB_ENV")
    with open(env_file, "a") as myfile:
        myfile.write(f"status={status}\ntask_score={task_score}\n")

test = None
if variant == 1:
    test = var1_test
else:
    write_task_res(f"Variant {variant} not found", 0)

if test is not None:
    try:
        task_score = test(decision)
    except Exception as e:
        write_task_res(f"Exception in decision function. Type: {type(e)}, messange: {str(e)}", 0)
    else:
        write_task_res("Done", task_score)
