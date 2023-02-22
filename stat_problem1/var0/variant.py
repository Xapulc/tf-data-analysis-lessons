from tools import ProblemVariant, SolutionTester, DescriptionGenerator, Singleton

problem1_variant0 = ProblemVariant("stat_task1_var0")


class SolutionTesterProblem1Variant0(SolutionTester):
    def __init__(self, code):
        self.code = code
        self.data_path = "stat_problem1/var0/sample.csv"
        self.score_list = [{
            "sample_size": 1000,
            "max_error": 0.01
        }, {
            "sample_size": 1000,
            "max_error": 0.005
        }, {
            "sample_size": 100,
            "max_error": 0.015
        }, {
            "sample_size": 10,
            "max_error": 0.09
        }]

    def get_code(self):
        return self.code

    def check_solution(self, solution, random_state):
        data = pd.read_csv(self.data_path)
        a_sample = data["a"]
        data_sample = data.drop(columns="a")

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


class DescriptionGeneratorProblem1Variant0(DescriptionGenerator):
    def __init__(self, code):
        self.code = code

        self.input_data_text = """
        \\section{Входные данные}
        Одномерный массив numpy.ndarray
        длин прыжков (в сантиметрах) одного спортсмена.
        """
        self.output_data_text = """
        \\section{Возвращаемое значение}
        Оценка матожидания длины прыжка.
        """
        self.estimation_text = """
        \\section{Оценка}
        Максимальный балл: $4$.
        \\begin{itemize}
        \\item $+1$ балл, если на выборках размера $1000$ MSE оценки $\leq 0.01$.
        \\item $+1$ балл, если на выборках размера $1000$ MSE оценки $\leq 0.005$.
        \\item $+1$ балл, если на выборках размера $100$ MSE оценки $\leq 0.015$.
        \\item $+1$ балл, если на выборках размера $10$ MSE оценки $\leq 0.09$.
        \\end{itemize}
        """
        self.problem_text = """
        \\section{Условие}
        Школа $N$ имеет сильный состав
        для соревнования в прыжках в длину.
        В ней есть несколько сильных спортсменов,
        но на соревнования нужно отправить одного.
        Тренер Максим вычитал из книги, 
        что длина прыжка имеет нормальное распределение,
        поэтому тренер решил выбрать лучшего школьника
        на основании оценки матожидания длины прыжка.
        Предполагая, что длины прыжков одного спортсмена
        независимы и имеют одинаковое для одного спортсмена распределение,
        помогите Максиму составить оценку этой величины
        для каждого студента.
        """

    def get_code(self):
        return self.code

    def get_description(self, random_state):
        return self.problem_text \
               + self.input_data_text \
               + self.output_data_text \
               + self.estimation_text
