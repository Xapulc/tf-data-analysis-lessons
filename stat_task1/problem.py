import pandas as pd

from ..tools import Problem


class StatProblem1(Problem):
    self.code = "stat_problem1"
    self.name = "Статистика, задание 1"
    self.max_score = 4
    self.problem_variant_list = [
    ]
    
    def __init__(self, user):
        self.user = user
    
    def get_description(self):
        
    
    def get_result_notification(self, task_score, test_result):
        score_data = pd.DataFrame(test_result)
        score_data["score"] = score_data.apply(lambda row : 1 if row["test_error"] <= row["max_error"] else 0,
                                               axis=1)
        score_data["test_error_format"] = score_data.apply(lambda row: "{:." + str(int(-np.log10(row["max_error"])) + 3) + "f}",
                                                           axis=1)
        score_data["test_error_str"] = score_data.apply(lambda row: row["test_error_format"].format(row["test_error"]), 
                                                        axis=1)
        column_description = [{
            "column": "sample_size",
            "description": "Размер выборки"
        }, {
            "column": "test_error_str",
            "description": "Среднеквадратичная ошибка решения"
        }, {
            "column": "max_error",
            "description": "Порог для среднеквадратичной ошибки решения"
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
            title_text=self.name,
            margin={
                "l": 0,
                "r": 0,
                "t": title_margin,
                "b": 0
            },
            width=700,
            height=cell_height * score_data.shape[0] + header_cell_height + title_margin
        )
        picture_path = "./" + self.code + ".png"
        fig.write_image(picture_path)

        message = f'В ДЗ "{self.name}" ваш общий результат: *{task_score} из {self.max_score}*.\n" \
                  + "Итоги проверки подведены в таблице."
        
        return message, [picture_path]
