import os
import pandas as pd
import plotly.graph_objects as go

from decimal import Decimal
from tools import Problem, Result, SolutionTester, DescriptionGenerator, \
                  round_down_first_decimal, round_up_first_decimal
from .var1 import hyp_problem1_variant1
from .var2 import hyp_problem1_variant2
from .var3 import hyp_problem1_variant3
from .var4 import hyp_problem1_variant4
from .var5 import hyp_problem1_variant5
from .var6 import hyp_problem1_variant6


hyp_problem1 = Problem(task_id="12755",
                       code="hyp_problem1",
                       name="Проверка гипотез, задание 1",
                       max_score=3,
                       criteria_list=[{
                           "sample_size": 1000,
                           "iter_size": 1000,
                           "error_factor": 1.1,
                           "delta_factor": Decimal("0")
                       }, {
                           "sample_size": 3000,
                           "iter_size": 1000,
                           "error_factor": 1.2,
                           "delta_factor": Decimal("-1")
                       }, {
                           "sample_size": 5000,
                           "iter_size": 1000,
                           "error_factor": 1.2,
                           "delta_factor": Decimal("1")
                       }],
                       problem_variant_list=[
                           hyp_problem1_variant1,
                           hyp_problem1_variant2,
                           hyp_problem1_variant3,
                           hyp_problem1_variant4,
                           hyp_problem1_variant5,
                           hyp_problem1_variant6
                       ])


class SolutionTesterHypProblem1(SolutionTester):
    def __init__(self, code, criteria_list):
        self.code = code
        self.criteria_list = criteria_list

    def get_code(self):
        return self.code

    def check_solution(self, solution, transformer_variant, random_state):
        result_list = []

        for criteria in self.criteria_list:
            true_hypothesis, control_p, control_sample, control_size, \
                test_p, test_sample, test_size = transformer_variant.get_sample(criteria["iter_size"],
                                                                                criteria["sample_size"],
                                                                                random_state,
                                                                                criteria["delta_factor"])
            total_error = 0
            for x_success, x_cnt, y_success, y_cnt in zip(control_sample,
                                                          control_size,
                                                          test_sample,
                                                          test_size):
                res = solution(x_success, x_cnt, y_success, y_cnt)

                if (true_hypothesis == 0) and res:
                    total_error += 1
                if (true_hypothesis == 1) and not res:
                    total_error += 1

            result_list.append({
                "sample_size": criteria["sample_size"],
                "true_hypothesis": true_hypothesis,
                "control_p": control_p,
                "test_p": test_p,
                "mean_error": total_error / criteria["iter_size"]
            })

        return result_list

    def generate_criteria(self, transformer_variant, random_state):
        generated_result_list = []
        result_list = self.check_solution(transformer_variant.get_solution(random_state),
                                          transformer_variant,
                                          random_state)

        for result, criteria in zip(result_list, self.criteria_list):
            max_error = result["mean_error"] * criteria["error_factor"]

            generated_result_list.append({
                "sample_size": result["sample_size"],
                "true_hypothesis": result["true_hypothesis"],
                "control_p": result["control_p"],
                "test_p": result["test_p"],
                "max_error": round_up_first_decimal(max_error, 2)
            })

        return generated_result_list


class DescriptionGeneratorHypProblem1(DescriptionGenerator):
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
        Выборка & $p$ на контроле & $p$ на тесте & Ошибка \\\\ [0.5ex]
        \\hline
        \\hline"""

        for criteria in generated_criteria_list:
            estimation_text += f"""
            ${criteria["sample_size"]}$ & ${criteria["control_p"]}$ & ${criteria["test_p"]}$ & ${criteria["max_error"]}$ \\\\
            \\hline"""

        estimation_text += """
        \\end{tabular}
        \\end{center}
        \\begin{itemize}
        \\item Выборка - Размер выборки
        \\item $p$ на контроле - Вероятность успеха на выборке из контроля
        \\item $p$ на тесте - Вероятность успеха на выборке из теста
        \\item Ошибка - Ограничение на частоту принятия неверного решения
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

    def get_solution_description(self, transformer_variant, generated_criteria_list, random_state):
        return transformer_variant.get_solution_description(random_state)


class ResultHypProblem1(Result):
    def __init__(self, code, name, max_score):
        self.code = code
        self.name = name
        self.max_score = max_score

    def get_code(self):
        return self.code

    def generate(self, test_result, generated_criteria_list):
        score_data = pd.DataFrame(data={
            "mean_error": [el["mean_error"] for el in test_result],
            "max_error": [el["max_error"] for el in generated_criteria_list],
            "sample_size": [el["sample_size"] for el in generated_criteria_list],
            "control_p": [el["control_p"] for el in generated_criteria_list],
            "test_p": [el["test_p"] for el in generated_criteria_list]
        })

        score_data["score"] = score_data.apply(lambda row : 1 if row["mean_error"] <= row["max_error"] else 0,
                                               axis=1)
        score_data["mean_error_rounded"] = score_data.apply(lambda row: round_down_first_decimal(row["mean_error"], 3),
                                                            axis=1)
        column_description = [{
            "column": "sample_size",
            "description": "Размер выборки"
        }, {
            "column": "control_p",
            "description": "Вероятность успеха на контроле"
        }, {
            "column": "test_p",
            "description": "Вероятность успеха на тесте"
        }, {
            "column": "mean_error_rounded",
            "description": "Частота неверного принятия решений"
        }, {
            "column": "max_error",
            "description": "Порог для частоты неверного принятия решений"
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
        message = f"В ДЗ ''{self.name}'' ваш общий результат: *{task_score} из {self.max_score}*.\n" \
                  + "Итоги проверки подведены в таблице."

        return task_score, message, [picture_path]
