import os
import pandas as pd
import plotly.graph_objects as go

from tools import Problem, Result, SolutionTester, DescriptionGenerator, \
                  round_down_first_decimal, round_up_first_decimal
from .var0 import problem1_variant0
from .var1 import problem1_variant1
from .var2 import problem1_variant2


problem1 = Problem(task_id="12277",
                   code="stat_problem1",
                   name="Статистика, задание 1",
                   max_score=4,
                   criteria_list=[{
                       "sample_size": 1000,
                       "iter_size": 1000,
                       "factor": 100
                   }, {
                       "sample_size": 1000,
                       "iter_size": 1000,
                       "factor": 10
                   }, {
                       "sample_size": 100,
                       "iter_size": 1000,
                       "factor": 3
                   }, {
                       "sample_size": 10,
                       "iter_size": 1000,
                       "factor": 1.1
                   }],
                   problem_variant_list=[
                       problem1_variant0,
                       problem1_variant1,
                       problem1_variant2
                   ])


class SolutionTesterProblem1(SolutionTester):
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

            for i in range(len(a)):
                a_est = solution(sample[i])
                total_error += (a[i] - a_est)**2

            result_list.append({
                "sample_size": criteria["sample_size"],
                "mean_error": total_error / criteria["iter_size"]
            })

        return result_list

    def generate_criteria(self, transformer_variant, random_state):
        generated_result_list = []
        result_list = self.check_solution(transformer_variant.get_solution(random_state),
                                          transformer_variant,
                                          random_state)

        for result, criteria in zip(result_list, self.criteria_list):
            max_error = result["mean_error"] * criteria["factor"]

            generated_result_list.append({
                "sample_size": result["sample_size"],
                "max_error": round_up_first_decimal(max_error, 2)
            })

        return generated_result_list


class DescriptionGeneratorProblem1(DescriptionGenerator):
    def __init__(self, code, max_score):
        self.code = code
        self.max_score = max_score

    def get_code(self):
        return self.code

    def _get_estimation_text(self, transformer_variant, generated_criteria_list, random_state):
        estimation_text = f"""
        Максимальный балл: ${self.max_score}$.
        \\begin{{itemize}}
        """

        for criteria in generated_criteria_list:
            estimation_text += f"""
        \\item $+1$ балл, если на выборках размера ${criteria["sample_size"]}$ MSE оценки $\\leq {criteria["max_error"]}$.
        """

        estimation_text += """
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


class ResultProblem1(Result):
    def __init__(self, code, name, max_score):
        self.code = code
        self.name = name
        self.max_score = max_score

    def get_code(self):
        return self.code

    def generate(self, test_result, generated_criteria_list):
        score_data = pd.DataFrame(data={
            "sample_size": [el["sample_size"] for el in test_result],
            "mean_error": [el["mean_error"] for el in test_result],
            "max_error": [el["max_error"] for el in generated_criteria_list]
        })
        score_data["score"] = score_data.apply(lambda row: 1 if row["mean_error"] <= row["max_error"] else 0,
                                               axis=1)
        score_data["mean_error_rounded"] = score_data.apply(lambda row: round_down_first_decimal(row["mean_error"], 3), axis=1)
        column_description = [{
            "column": "sample_size",
            "description": "Размер выборки"
        }, {
            "column": "mean_error_rounded",
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
