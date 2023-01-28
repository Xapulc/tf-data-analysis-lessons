import os
import pandas as pd 
import numpy as np


def score(test_stat: dict) -> int:
    total_score = 0

    if test_stat[1000]["mean_error"] < 0.01:
        total_score += 1

    if test_stat[1000]["mean_error"] < 0.001:
        total_score += 1

    if test_stat[100]["mean_error"] < 0.00015:
        total_score += 1

    if test_stat[10]["mean_error"] < 0.0011:
        total_score += 1

    return total_score
  
  
def test(decision) -> int:
    data = pd.read_csv("task1/var1/sample.csv")
    a_sample = data["a"]
    data_sample = data.drop(columns="a")

    test_stat = {}
    sample_size_error = {}
    sample_size_number = {}
    sample_size_result = {}

    for i in range(len(a_sample)):
        a = a_sample[i]
        v = data_sample.iloc[i].dropna().to_numpy()
        sample_size = len(v)

        a_est = decision(v)
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
