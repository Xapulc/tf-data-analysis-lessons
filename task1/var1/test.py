import os
import pandas as pd 
import numpy as np
  
  
def test(solution) -> int:
    data = pd.read_csv("task1/var1/sample.csv")
    a_sample = data["a"]
    data_sample = data.drop(columns="a")
    
    score_list = [{
        "sample_size": 1000,
        "max_error": 0.001
    }, {
        "sample_size": 1000,
        "max_error": 0.0001
    }, {
        "sample_size": 100,
        "max_error": 0.00015
    }, {
        "sample_size": 10,
        "max_error": 0.0011
    }]

    test_stat = {}
    
    sample_size_error = {}
    sample_size_number = {}
    sample_size_result = {}

    for i in range(len(a_sample)):
        a = a_sample[i]
        v = data_sample.iloc[i].dropna().to_numpy()
        sample_size = len(v)

        a_est = solution(v)
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
        
    for score_element in score_list:
        score_element["test_error"] = test_stat[score_element["sample_size"]]["mean_error"]
    
    return score_list
