import os
import pandas as pd 
import numpy as np
  
  
def test(solution) -> list:
    data = pd.read_csv("stat_problem2/var0/sample.csv")
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
    
    for i in range(len(a_sample)):
        a = a_sample[i]
        x = data_sample.iloc[i].dropna().to_numpy()
        sample_size = len(x)
        
        for score_element in score_list:
            if sample_size != score_element["sample_size"]:
                continue
            
            left_side, right_side = solution(score_element["confidence"], x)
            interval_length = np.abs(right_side - left_side)
            error = 1 if (a < left_side or right_side < a) else 0
        
            score_element["total_error"] = score_element.get("total_error", 0) + error
            score_element["total_interval_length"] = score_element.get("total_interval_length", 0) + interval_length
            score_element["number"] = score_element.get("number", 0) + 1
    
    for score_element in score_list:
        score_element["mean_error"] = score_element["total_error"] / score_element["number"]
        score_element["mean_interval_length"] = score_element["total_interval_length"] / score_element["number"]

    return score_list
