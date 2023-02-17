import os
import pandas as pd 
import numpy as np


def score(test_stat: dict) -> int:
    total_score = 0

    if test_stat[0.99][1000]["mean_error"] < 0.02 and test_stat[0.99][1000]["mean_interval_length"] < 2:
        total_score += 1

    if test_stat[0.9][1000]["mean_error"] < 0.12 and test_stat[0.9][1000]["mean_interval_length"] < 1.1:
        total_score += 1

    if test_stat[0.7][100]["mean_error"] < 0.32 and test_stat[0.7][100]["mean_interval_length"] < 2.2:
        total_score += 1

    if test_stat[0.9][100]["mean_error"] < 0.11 and test_stat[0.9][100]["mean_interval_length"] < 3.3:
        total_score += 1

    if test_stat[0.95][10]["mean_error"] < 0.1 and test_stat[0.95][10]["mean_interval_length"] < 13:
        total_score += 1

    if test_stat[0.9][10]["mean_error"] < 0.11 and test_stat[0.9][10]["mean_interval_length"] < 10.6:
        total_score += 1

    return total_score
  
  
def test(solution) -> int:
    data = pd.read_csv("stat_task2/var0/sample.csv")
    a_sample = data["a"]
    data_sample = data.drop(columns="a")
    score_list = [{
        "sample_size": 1000,
        "confidence": 0.99,
        "max_error": 0.02,
        "max_interval_length": 2
    }, {
        "sample_size": 1000,
        "confidence": 0.9,
        "max_error": 0.12,
        "max_interval_length": 1.1
    }, {
        "sample_size": 100,
        "confidence": 0.7,
        "max_error": 0.32,
        "max_interval_length": 2.2
    }, {
        "sample_size": 100,
        "confidence": 0.9,
        "max_error": 0.11,
        "max_interval_length": 3.3
    }, {
        "sample_size": 10,
        "confidence": 0.95,
        "max_error": 0.1,
        "max_interval_length": 13
    }, {
        "sample_size": 10,
        "confidence": 0.9,
        "max_error": 0.11,
        "max_interval_length": 10.6
    }]

    for p in test_stat.keys():
        for sample_size in test_stat[p].keys():
            test_stat[p][sample_size]["total_error"] = 0
            test_stat[p][sample_size]["total_interval_length"] = 0
            test_stat[p][sample_size]["number"] = 0

        for i in range(len(a_sample)):
            a = a_sample[i]
            x = data_sample.iloc[i].dropna().to_numpy()
            sample_size = len(x)

            left_side, right_side = solution(p, x)
            interval_length = np.abs(right_side - left_side)
            error = 1 if (a < left_side or right_side < a) else 0

            if sample_size in test_stat[p].keys():
                test_stat[p][sample_size]["total_error"] += error
                test_stat[p][sample_size]["total_interval_length"] += interval_length
                test_stat[p][sample_size]["number"] += 1

        for sample_size in test_stat[p].keys():
            test_stat[p][sample_size]["mean_error"] = test_stat[p][sample_size]["total_error"] \
                                                      / test_stat[p][sample_size]["number"]
            test_stat[p][sample_size]["mean_interval_length"] = test_stat[p][sample_size]["total_interval_length"] \
                                                                / test_stat[p][sample_size]["number"]

    return score(test_stat)
