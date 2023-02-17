import numpy as np
import pandas as pd
import plotly.graph_objects as go

from .var0.test import test as var0_test
from .var1.test import test as var1_test


max_score = 6
salt = "stat_task2"
min_variant = 0
max_variant = 1

def check_solution(variant, solution):
    test = None
    if variant == 0:
        test = var0_test
    elif variant == 1:
        test = var1_test
    else:
        return 0, f"Вариант {variant} не найден", "Error"
    
    try:
        score_list = test(solution)
    except Exception as e:
        return 0, f"Ошибка в решающей функции. Тип ошибки: {type(e)}, сообщение ошибки: {str(e)}", "Error"
   
    message = f"В задании 2 у вас *{variant}-й вариант*.\n"
    task_score = 0
    
    for score_element in score_list:
        score = 0
        if score_element["mean_error"] <= score_element["max_error"] \
                and score_element["mean_interval_length"] <= score_element["max_interval_length"]:
            score = 1
            
        task_score += score
        
        message += f"• На выборках размера `{score_element['sample_size']}` " \
                   + f"и с уровнем доверия `{score_element['confidence']}` "

        mean_error_format = "{:." + str(int(-np.log10(score_element["max_error"])) + 3) + "f}"
        mean_error_str = mean_error_format.format(score_element["mean_error"])
        
        message += f"частота непопадания в доверительный интервал равна `{mean_error_str}` " \
                   + f"при пороге `{score_element['max_error']}`, "

        mean_interval_length_format = "{:." + str(int(-np.log10(score_element["max_interval_length"])) + 3) + "f}"
        mean_interval_length_str = mean_interval_length_format.format(score_element["mean_interval_length"])
        
        message += f"средняя длина доверительного интервала равна `{mean_interval_length_str}` " \
                   + f"при пороге `{score_element['max_interval_length']}`. "
        message += f"За этот пункт вы получаете количество баллов = {score}.\n"
        
    message += f"Ваш общий результат: *{task_score} из {max_score}*."
    
    score_data = pd.DataFrame(score_list)
    score_data["score"] = score_data.apply(lambda row : 1 if (row["mean_error"] <= row["max_error"]
                                                              and row["mean_interval_length"] <= row["max_interval_length"])
                                                        else 0,
                                           axis=1)
    score_data["mean_error_format"] = score_data.apply(lambda row: "{:." + str(int(-np.log10(row["max_error"])) + 3) + "f}",
                                                       axis=1)
    score_data["mean_error_str"] = score_data.apply(lambda row: row["mean_error_format"].format(row["mean_error"]), 
                                                    axis=1)
    score_data["mean_interval_length_format"] = score_data.apply(lambda row: "{:." + str(int(-np.log10(row["max_interval_length"])) + 3) + "f}",
                                                                 axis=1)
    score_data["mean_interval_length_str"] = score_data.apply(lambda row: row["mean_interval_length_format"].format(row["mean_interval_length"]), 
                                                              axis=1)
    column_description = [{
        "column": "sample_size",
        "description": "Размер выборки"
    }, {
        "column": "confidence",
        "description": "Уровень доверия"
    }, {
        "column": "mean_error_str",
        "description": "Частота непопадания в доверительный интервал"
    }, {
        "column": "max_error",
        "description": "Порог для частоты непопадания в доверительный интервал"
    }, {
        "column": "mean_interval_length_str",
        "description": "Средняя длина доверительного интервала"
    }, {
        "column": "max_interval_length",
        "description": "Порог длины доверительного интервала"
    }, {
        "column": "score",
        "description": "Балл"
    }]
    
    score_data = score_data[[el["column"] for el in column_description]] \
                           .rename(columns={el["column"]: el["description"] for el in column_description})
    
    color_function = lambda score: "rgba(114, 220, 140, 0.5)" if score == 1 else "rgba(240, 113, 111, 0.5)"
    fig = go.Figure(go.Table(header={"values": list(score_data.columns)},
                             cells={
                                 "values": score_data.values.transpose(),
                                 "fill_color": [score_data["Балл"].apply(color_function)]
                             }))
    fig.update_layout(
        autosize=False,
        margin={
            "l": 0,
            "r": 0,
            "t": 0,
            "b": 0
        }
    )
    picture_path = "./" + salt + ".png"
    fig.write_image(picture_path)
   
    return task_score, message, "Done", [picture_path]
