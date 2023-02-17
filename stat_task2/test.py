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
    cell_height = 30
    header_cell_height = 70
    
    fig = go.Figure(go.Table(header={
                                 "values": list(score_data.columns),
                                 "height": header_cell_height
                             },
                             cells={
                                 "values": score_data.values.transpose(),
                                 "fill_color": [score_data["Балл"].apply(color_function)],
                                 "height": cell_height
                             }))
    title_margin = 50
    fig.update_layout(
        title_text="Задание 2",
        margin={
            "l": 0,
            "r": 0,
            "t": title_margin,
            "b": 0
        },
        width=1000,
        height=cell_height * score_data.shape[0] + header_cell_height + title_margin
    )
    picture_path = "./" + salt + ".png"
    fig.write_image(picture_path)

    task_score = score_data["Балл"].sum()
    message = f"В задании 2 у вас *{variant}-й вариант*.\n" \
              + f"Ваш общий результат: *{task_score} из {max_score}*.\n" \
              + "Итоги проверки подведены в таблице."
   
    return task_score, message, "Done", [picture_path]
