import os
import pandas as pd 
import numpy as np

from test1.var1.

from student_work.task1 import decision



def write_task_res(status, max_score, task_score):
  env_file = os.getenv('GITHUB_ENV')
  with open(env_file, "a") as myfile:
    myfile.write(f"status={status}\nmax_score={max_score}\ntask_score={task_score}\n")

data = pd.read_csv('test1_data.csv')
data["student_res"] = data.apply(lambda row: student_sum(row["a"], row["b"]), axis=1)
suc_cnt = np.where(data["student_res"] == data["res"], 1, 0).sum()

write_task_res("Done", 10, int(10 * suc_cnt / data.shape[0]))
