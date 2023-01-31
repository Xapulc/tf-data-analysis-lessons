import os
import pandas as pd 
import numpy as np


def score(test_stat: dict) -> int:
    total_score = 0

    if test_stat[1000]["mean_error"] < 0.03:
        total_score += 1

    if test_stat[1000]["mean_error"] < 0.01:
        total_score += 1

    if test_stat[100]["mean_error"] < 0.05:
        total_score += 1

    if test_stat[10]["mean_error"] < 0.25:
        total_score += 1

    return total_score
  
  
def test(solution) -> int:
    data = pd.read_csv("task1/var3/sample.csv")
    a_sample = data["a"]
    data_sample = data.drop(columns="a")

    test_stat = {}
    sample_size_error = {}
    sample_size_number = {}
    sample_size_result = {}

    for i in range(len(a_sample)):
        a = a_sample[i]
        x = data_sample.iloc[i].dropna().to_numpy()
        sample_size = len(x)

        a_est = solution(x)
        error = (a - a_est)**2

        if sample_size in test_stat.keys():
            test_stat[sample_size]["total_error"] += error
            test_stat[sample_size]["number"] += 1
        else:
            test_stat[sample_size] = {}
            test_stat[sample_size]["total_error"] = error
            test_stat[sample_size]["number"] = 1

    for sample_size in test_stat.keys():
        test_stat[sample_size]["mean_error"] = test_stat[sample_size]["total_error"] \
                                               / test_stat[sample_size]["number"]
    
    return score(test_stat)
