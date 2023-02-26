import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from tools import Problem, Result, SolutionTester, DescriptionGenerator, \
                  round_down_first_decimal, round_up_first_decimal
from .var0 import problem2_variant0
from .var1 import problem2_variant1
from .var2 import problem2_variant2


problem2 = Problem(task_id="12559",
                   code="stat_problem2",
                   name="Статистика, задание 2",
                   max_score=6,
                   criteria_list=[{
                       "sample_size": 1000,
                       "confidence": 0.99,
                       "iter_size": 1000,
                       "error_factor_type": "max",
                       "error_factor": 10,
                       "length_factor_type": "max",
                       "length_factor": 20
                   }, {
                       "sample_size": 1000,
                       "confidence": 0.9,
                       "iter_size": 1000,
                       "error_factor_type": "max",
                       "error_factor": 5,
                       "length_factor_type": "max",
                       "length_factor": 10
                   }, {
                       "sample_size": 100,
                       "confidence": 0.7,
                       "iter_size": 1000,
                       "error_factor_type": "max",
                       "error_factor": 1.5,
                       "length_factor_type": "max",
                       "length_factor": 2
                   }, {
                       "sample_size": 100,
                       "confidence": 0.9,
                       "iter_size": 1000,
                       "error_factor_type": "exact",
                       "error_factor": 1.02,
                       "length_factor_type": "exact",
                       "length_factor": 1.2
                   }, {
                       "sample_size": 10,
                       "confidence": 0.95,
                       "iter_size": 1000,
                       "error_factor_type": "max",
                       "error_factor": 1.3,
                       "length_factor_type": "max",
                       "length_factor": 1.5
                   }, {
                       "sample_size": 10,
                       "confidence": 0.9,
                       "iter_size": 1000,
                       "error_factor_type": "exact",
                       "error_factor": 1.1,
                       "length_factor_type": "exact",
                       "length_factor": 1.1
                   }],
                   problem_variant_list=[
                       problem2_variant0,
                       problem2_variant1,
                       problem2_variant2
                   ])


class SolutionTesterProblem2(SolutionTester):
    def __init__(self, code, criteria_list):
        self.code = code
        self.criteria_list = criteria_list

    def get_code(self):
        return self.code

    def check_solution(self, solution, transformer_variant, random_state):
        result_list = []

        for criteria in self.criteria_list:
            sample, a = transformer_variant.get_sample(criteria["iter_size"],
                                                       criteria["sample_size"],
                                                       random_state)
            total_error = 0
            total_interval_length = 0

            for i in range(len(a)):
                left_side, right_side = solution(criteria["confidence"], sample[i])
                total_error += (1 if (a[i] < left_side or right_side < a[i]) else 0)
                total_interval_length += np.abs(right_side - left_side)

            result_list.append({
                "sample_size": criteria["sample_size"],
                "mean_error": total_error / criteria["iter_size"],
                "mean_interval_length": total_interval_length / criteria["iter_size"]
            })

        return result_list

    def generate_criteria(self, transformer_variant, random_state):
        generated_result_list = []
        exact_result_list = self.check_solution(transformer_variant.get_exact_solution(random_state),
                                                transformer_variant,
                                                random_state)
        clt_result_list = self.check_solution(transformer_variant.get_clt_solution(random_state),
                                              transformer_variant,
                                              random_state)

        for exact_result, clt_result, criteria in zip(exact_result_list,
                                                      clt_result_list,
                                                      self.criteria_list):
            if criteria["error_factor_type"] == "max":
                max_error = max(exact_result["mean_error"], clt_result["mean_error"])
            elif criteria["error_factor_type"] == "exact":
                max_error = exact_result["mean_error"]
            else:
                max_error = clt_result["mean_error"]
            max_error *= criteria["error_factor"]

            if criteria["length_factor_type"] == "max":
                max_interval_length = max(exact_result["mean_interval_length"], clt_result["mean_interval_length"])
            elif criteria["length_factor_type"] == "exact":
                max_interval_length = exact_result["mean_interval_length"]
            else:
                max_interval_length = clt_result["mean_interval_length"]
            max_interval_length *= criteria["length_factor"]

            generated_result_list.append({
                "sample_size": criteria["sample_size"],
                "confidence": criteria["confidence"],
                "max_error": round_up_first_decimal(max_error, 2),
                "max_interval_length": round_up_first_decimal(max_interval_length, 2)
            })

        return generated_result_list


class DescriptionGeneratorProblem2(DescriptionGenerator):
    def __init__(self, code, max_score):
        self.code = code
        self.max_score = max_score

    def get_code(self):
        return self.code

    def _get_estimation_text(self, transformer_variant, generated_criteria_list, random_state):
        estimation_text = f"""
        Максимальный балл: ${self.max_score}$.
        \\begin{{center}}
        \\begin{{tabular}}{{||c c c c||}} 
        \\hline
        Выборка & Доверие & Частота ошибок & Длина интервала \\\\ [0.5ex]
        \\hline
        \\hline"""

        for criteria in generated_criteria_list:
            estimation_text += f"""
            ${criteria["sample_size"]}$ & ${criteria["confidence"]}$ & ${criteria["max_error"]}$ & ${criteria["max_interval_length"]}$ \\\\
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

    def get_description(self, transformer_variant, generated_criteria_list, random_state):
        description = transformer_variant.get_description(random_state)
        return f"""
        \\section{{Условие}} {description["problem"]}
        \\section{{Входные данные}} {description["input"]}
        \\section{{Возвращаемое значение}} {description["output"]}
        \\section{{Оценка}} {self._get_estimation_text(transformer_variant, generated_criteria_list, random_state)}
        """


class ResultProblem2(Result):
    def __init__(self, code, name, max_score):
        self.code = code
        self.name = name
        self.max_score = max_score

    def get_code(self):
        return self.code

    def generate(self, test_result, generated_criteria_list):
        score_data = pd.DataFrame(data={
            "mean_error": [el["mean_error"] for el in test_result],
            "mean_interval_length": [el["mean_interval_length"] for el in test_result],
            "max_error": [el["max_error"] for el in generated_criteria_list],
            "max_interval_length": [el["max_interval_length"] for el in generated_criteria_list],
            "sample_size": [el["sample_size"] for el in generated_criteria_list],
            "confidence": [el["confidence"] for el in generated_criteria_list]
        })

        score_data["score"] = score_data.apply(lambda row : 1 if (row["mean_error"] <= row["max_error"]
                                                                  and row["mean_interval_length"] <= row["max_interval_length"])
                                                            else 0,
                                               axis=1)
        score_data["mean_error_rounded"] = score_data.apply(lambda row: round_down_first_decimal(row["mean_error"], 3),
                                                            axis=1)
        score_data["mean_interval_length_rounded"] = score_data.apply(lambda row: round_down_first_decimal(row["mean_interval_length"], 3),
                                                                      axis=1)
        column_description = [{
            "column": "sample_size",
            "description": "Размер выборки"
        }, {
            "column": "confidence",
            "description": "Уровень доверия"
        }, {
            "column": "mean_error_rounded",
            "description": "Частота непопадания в доверительный интервал"
        }, {
            "column": "max_error",
            "description": "Порог для частоты непопадания в доверительный интервал"
        }, {
            "column": "mean_interval_length_rounded",
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

        current_path = os.path.dirname(os.path.dirname(__file__))
        tmp_dir = os.path.join(current_path, "tmp/")
        os.makedirs(tmp_dir, exist_ok=True)
        picture_path = os.path.join(tmp_dir, self.code + ".png")
        fig.write_image(picture_path)

        task_score = score_data["Балл"].sum()
        message = f'В ДЗ "{self.name}" ваш общий результат: *{task_score} из {self.max_score}*.\n' \
                  + "Итоги проверки подведены в таблице."

        return task_score, message, [picture_path]
