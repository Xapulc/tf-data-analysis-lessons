import pandas as pd

from tools import ProblemVariant, SolutionTester, DescriptionGenerator


problem1_variant1 = ProblemVariant("stat_task1_var1")


class SolutionTesterProblem1Variant1(SolutionTester):
    def __init__(self, code):
        self.code = code
        self.data_path = "stat_problem1/var1/sample.csv"
        self.score_list = [{
            "sample_size": 1000,
            "max_error": 0.001
        }, {
            "sample_size": 1000,
            "max_error": 0.0001
        }, {
            "sample_size": 100,
            "max_error": 0.00015
        }, {
            "sample_size": 10,
            "max_error": 0.0011
        }]

    def get_code(self):
        return self.code

    def check_solution(self, solution, random_state):
        # Выборка была получена при eps(i) ~ -2+exp(1)
        data = pd.read_csv(self.data_path)
        a_sample = data["a"]
        data_sample = data.drop(columns="a")

        min_exp_deviation = -1
        max_exp_deviation = 50
        exp_deviation = min_exp_deviation + (random_state % (max_exp_deviation - min_exp_deviation + 1))
        print(2+exp_deviation)
        test_stat = {}

        for i in range(len(a_sample)):
            a = a_sample[i]
            data_row = data_sample.iloc[i].dropna().to_numpy()
            sample_size = len(data_row)

            a_est = solution(data_row - exp_deviation)
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

        for score_element in self.score_list:
            score_element["test_error"] = test_stat[score_element["sample_size"]]["mean_error"]

        return self.score_list


class DescriptionGeneratorProblem1Variant1(DescriptionGenerator):
    def __init__(self, code):
        self.code = code

        self.input_data_text = """
        \\section{Входные данные}
        Одномерный массив numpy.ndarray
        измерений скорости (в м/c) машин одной модели.
        """
        self.output_data_text = """
        \\section{Возвращаемое значение}
        Оценка коэффициента ускорения (в м/с^2).
        """
        self.estimation_text = """
        \\section{Оценка}
        Максимальный балл: $4$.
        \\begin{itemize}
        \\item $+1$ балл, если на выборках размера $1000$ MSE оценки $\leq 0.001$.
        \\item $+1$ балл, если на выборках размера $1000$ MSE оценки $\leq 0.0001$.
        \\item $+1$ балл, если на выборках размера $100$ MSE оценки $\leq 0.00015$.
        \\item $+1$ балл, если на выборках размера $10$ MSE оценки $\leq 0.0011$.
        \\end{itemize}
        """

    def get_code(self):
        return self.code

    def get_description(self, random_state):
        min_exp_deviation = -1
        max_exp_deviation = 50
        exp_deviation = min_exp_deviation + (random_state % (max_exp_deviation - min_exp_deviation + 1))

        problem_text = """
        \\section{Условие}
        На заводе проводится тестирование модели машины для проверки коэффициента ускорения. 
        В рамках эксперимента выбирается $n$ машин этой модели 
        и измеряется скорость машины через $10$ секунд.
        Предполагается, что ошибки измерения скорости н.о.р.
        """ + f"""
        и имеют распределение ${-2-exp_deviation} + exp(1)$.
        Постройте точечную оценку коэффициента ускорения.
        """
        return problem_text \
               + self.input_data_text \
               + self.output_data_text \
               + self.estimation_text
