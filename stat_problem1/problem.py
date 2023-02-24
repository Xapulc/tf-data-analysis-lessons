import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from tools import Problem, Result, SolutionTester, DescriptionGenerator
from .var0 import problem1_variant0
from .var1 import problem1_variant1


problem1 = Problem(task_id="12277",
                   code="stat_problem1",
                   name="Статистика, задание 1",
                   max_score=4,
                   problem_variant_list=[
                       problem1_variant0,
                       problem1_variant1
                   ])


class DescriptionGeneratorProblem1(DescriptionGenerator):
    def __init__(self, code, max_score):
        self.code = code
        self.max_score = max_score

    def get_code(self):
        return self.code

    def _get_estimation_text(self, transformer_variant, random_state):
        score_list = transformer_variant.get_score_list(random_state)
        estimation_text = f"""
        Максимальный балл: ${self.max_score}$.
        \\begin{{itemize}}
        """

        for score in score_list:
            estimation_text += f"""
        \\item $+1$ балл, если на выборках размера ${score["sample_size"]}$ MSE оценки $\\leq {score["max_error"]}$.
        """

        estimation_text += """
        \\end{itemize}
        """
        return estimation_text

    def get_description(self, transformer_variant, random_state):
        description = transformer_variant.get_description(random_state)
        return f"""
        \\section{{Условие}} {description["problem"]}
        \\section{{Входные данные}} {description["input"]}
        \\section{{Возвращаемое значение}} {description["output"]}
        \\section{{Оценка}} {self._get_estimation_text(transformer_variant, random_state)}
        """


class SolutionTesterProblem1(SolutionTester):
    def __init__(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def check_solution(self, solution, transformer_variant, random_state):
        data_sample, a_sample = transformer_variant.get_sample(random_state)
        score_list = transformer_variant.get_score_list(random_state)
        test_stat = {}

        for i in range(len(a_sample)):
            a = a_sample[i]
            data_row = data_sample.iloc[i].dropna().to_numpy()
            sample_size = len(data_row)

            a_est = solution(data_row)
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


class ResultProblem1(Result):
    def __init__(self, code, name, max_score):
        self.code = code
        self.name = name
        self.max_score = max_score

    def get_code(self):
        return self.code

    def generate(self, test_result):
        score_data = pd.DataFrame(test_result)
        score_data["score"] = score_data.apply(lambda row: 1 if row["test_error"] <= row["max_error"] else 0,
                                               axis=1)
        score_data["test_error_format"] = score_data.apply(
            lambda row: "{:." + str(int(-np.log10(row["max_error"])) + 3) + "f}",
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

        color_function = lambda score: ("rgba(114, 220, 140, 0.5)" if score == 1 else "rgba(240, 113, 111, 0.5)")
        cell_height = 30
        header_cell_height = 70

        fig = go.Figure(go.Table(header={
            "values": list(score_data.columns),
            "height": header_cell_height
        }, cells={
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

        current_path = os.path.dirname(os.path.dirname(__file__))
        tmp_dir = os.path.join(current_path, "tmp/")
        os.makedirs(tmp_dir, exist_ok=True)
        picture_path = os.path.join(tmp_dir, self.code + ".png")
        fig.write_image(picture_path)

        task_score = score_data["Балл"].sum()
        message = f'В ДЗ "{self.name}" ваш общий результат: *{task_score} из {self.max_score}*.\n' \
                  + "Итоги проверки подведены в таблице."

        return task_score, message, [picture_path]
