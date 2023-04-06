import os
import pandas as pd
import plotly.graph_objects as go

from tools import Problem, Result, SolutionTester, DescriptionGenerator, \
                  round_down_first_decimal, round_up_first_decimal
from .var1 import hyp_problem2_variant1
from .var2 import hyp_problem2_variant2
from .var3 import hyp_problem2_variant3
from .var4 import hyp_problem2_variant4
from .var5 import hyp_problem2_variant5


hyp_problem2 = Problem(task_id="13782",
                       code="hyp_problem2",
                       name="Проверка гипотез, задание 2",
                       max_score=4,
                       criteria_list=[{
                           "sample_size": 300,
                           "iter_size": 500,
                           "y_dist_num": 0,
                           "error_factor": 1.1
                       }, {
                           "sample_size": 300,
                           "iter_size": 500,
                           "y_dist_num": 1,
                           "error_factor": 1.1
                       }, {
                           "sample_size": 300,
                           "iter_size": 500,
                           "y_dist_num": 2,
                           "error_factor": 1.1
                       }, {
                           "sample_size": 300,
                           "iter_size": 500,
                           "y_dist_num": 3,
                           "error_factor": 1.1
                       }],
                       problem_variant_list=[
                           hyp_problem2_variant1,
                           hyp_problem2_variant2,
                           hyp_problem2_variant3,
                           hyp_problem2_variant4,
                           hyp_problem2_variant5
                       ])


class SolutionTesterHypProblem2(SolutionTester):
    def __init__(self, code, criteria_list):
        self.code = code
        self.criteria_list = criteria_list

    def get_code(self):
        return self.code

    def check_solution(self, solution, transformer_variant, random_state):
        result_list = []

        for criteria in self.criteria_list:
            x_sample_list, y_sample_list = transformer_variant.get_sample(criteria["iter_size"],
                                                                          criteria["sample_size"],
                                                                          random_state,
                                                                          criteria["y_dist_num"])
            total_error = 0
            for x, y in zip(x_sample_list,
                            y_sample_list):
                res = solution(x, y)

                if (criteria["y_dist_num"] == 0) and res:
                    total_error += 1
                if (criteria["y_dist_num"] != 0) and not res:
                    total_error += 1

            result_list.append({
                "sample_size": criteria["sample_size"],
                "y_dist_num": criteria["y_dist_num"],
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
                "y_dist_num": result["y_dist_num"],
                "max_error": round_up_first_decimal(max_error, 2)
            })

        return generated_result_list


class DescriptionGeneratorHypProblem2(DescriptionGenerator):
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
        $X$ & $Y$ & Выборка & Ошибка \\\\ [0.5ex]
        \\hline
        \\hline"""

        for criteria in generated_criteria_list:
            x_dist_desc = "Историческое"
            if criteria["y_dist_num"] == 0:
                y_dist_desc = "Историческое"
            else:
                y_dist_desc = f"Изменённое типа {criteria['y_dist_num']}"

            estimation_text += f"""
            {x_dist_desc} & {y_dist_desc} & ${criteria["sample_size"]}$ & ${criteria["max_error"]}$ \\\\
            \\hline"""

        estimation_text += """
        \\end{tabular}
        \\end{center}
        \\begin{itemize}
        \\item $X$ - Распределение выборки $X$
        \\item $Y$ - Распределение выборки $Y$
        \\item Выборка - Размер выборки
        \\item Ошибка - Ограничение на частоту принятия неверного решения
        \\end{itemize}
        """

        return estimation_text

    def _get_example_sample(self, transformer_variant, iter_size, sample_size, random_state):
        file_name_list = []

        for el in transformer_variant.get_example_sample(iter_size, sample_size, random_state-535131):
            sample = pd.DataFrame(data=el["data"],
                                  columns=[f"x{i}" for i in range(sample_size)])
            file_name = "tmp/historical_data.csv" if el["dist_num"] == 0 \
                        else f"tmp/modified_data_of_type_{el['dist_num']}.csv"
            sample.to_csv(file_name)
            file_name_list.append(file_name)

        return file_name_list

    def get_description(self, transformer_variant, generated_criteria_list, random_state):
        description = transformer_variant.get_description(random_state)
        file_name_list = self._get_example_sample(transformer_variant, 200, 300, random_state)

        return f"""
        \\section{{Условие}} {description["problem"]}
        \\section{{Входные данные}} {description["input"]}
        \\section{{Возвращаемое значение}} {description["output"]}
        \\section{{Оценка}} {self._get_estimation_text(transformer_variant, generated_criteria_list, random_state)}
        """, file_name_list


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
            "y_dist_num": [el["y_dist_num"] for el in generated_criteria_list]
        })

        score_data["score"] = score_data.apply(lambda row : 1 if row["mean_error"] <= row["max_error"] else 0,
                                               axis=1)
        score_data["mean_error_rounded"] = score_data.apply(lambda row: round_down_first_decimal(row["mean_error"], 3),
                                                            axis=1)
        score_data["dist_desc"] = score_data.apply(lambda row: "Историческое VS Историческое" if row["y_dist_num"] == 0
                                                               else f"Историческое VS Изменённое типа {row['y_dist_num']}",
                                                   axis=1)
        column_description = [{
            "column": "sample_size",
            "description": "Размер выборки"
        }, {
            "column": "dist_desc",
            "description": "Описание распределений"
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
