import pandas as pd
import numpy as np
import plotly.graph_objects as go

from tools import Problem, Result, SolutionTester, DescriptionGenerator
from .var0 import problem2_variant0


problem2 = Problem(task_id="12559",
                   code="stat_problem2",
                   name="Статистика, задание 2",
                   max_score=6,
                   problem_variant_list=[
                       problem2_variant0
                   ])


class DescriptionGeneratorProblem2(DescriptionGenerator):
    def __init__(self, code, max_score):
        self.code = code
        self.max_score = max_score

    def get_code(self):
        return self.code

    def _get_estimation_text(self, transformer_variant, random_state):
        score_list = transformer_variant.get_score_list(random_state)
        estimation_text = f"""
        Максимальный балл: ${self.max_score}$.
        \\begin{{center}}
        \\begin{{tabular}}{{||c c c c||}} 
        \\hline
        Выборка & Доверие & Частота ошибок & Длина интервала \\\\ [0.5ex]
        \\hline
        \\hline"""

        for score in score_list:
            estimation_text += f"""
            ${score["sample_size"]}$ & ${score["confidence"]}$ & ${score["max_error"]}$ & ${score["max_interval_length"]}$ \\\\
            \\hline"""

        estimation_text += """
        \\end{tabular}
        \\end{center}
        \\begin{itemize}
        \\item Выборка - Размер выборки
        \\item Доверие - Уровень доверия
        \\item Частота ошибок - Ограничение на частоту непопадания в доверительный интервал
        \\item Длина интервала - Ограничение на среднюю длину доверительного интервала
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


class SolutionTesterProblem2(SolutionTester):
    def __init__(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def check_solution(self, solution, transformer_variant, random_state):
        data_sample, a_sample = transformer_variant.get_sample(random_state)
        score_list = transformer_variant.get_score_list(random_state)

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


class ResultProblem2(Result):
    def __init__(self, code, name, max_score):
        self.code = code
        self.name = name
        self.max_score = max_score

    def get_code(self):
        return self.code

    def generate(self, test_result):
        score_data = pd.DataFrame(test_result)
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
            width=1000,
            height=cell_height * score_data.shape[0] + header_cell_height + title_margin
        )
        picture_path = "tmp/" + self.code + ".png"
        fig.write_image(picture_path)

        task_score = score_data["Балл"].sum()
        message = f'В ДЗ "{self.name}" ваш общий результат: *{task_score} из {self.max_score}*.\n' \
                  + "Итоги проверки подведены в таблице."

        return task_score, message, [picture_path]
