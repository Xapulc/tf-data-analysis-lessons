import numpy as np

from decimal import Decimal
from hyppo.ksample import MMD
from scipy.stats import norm, laplace
from tools import ProblemVariant, VariantTransformer


hyp_problem2_variant3 = ProblemVariant(code="hyp_task2_var3",
                                       input_data_text="""
                                       Две выборки параметра $F$.
                                       """,
                                       output_data_text=r"""
                                       bool-значение, ответ на вопрос: 
                                       "Отклонить ли гипотезу однородности выборок"
                                       на заданном уровне значимости.
                                       """)


class TransformerHypProblem2Variant3(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

        self.null_dist = norm(0, 1)
        self.first_dist = laplace(scale=1 / np.sqrt(2))
        self.second_dist = norm(0, 0.8)
        self.third_dist = norm(0.2, 0.9)

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 1
        max_alpha_numerator = 10
        alpha_denominator = 100

        alpha_numerator = min_alpha_numerator + ((random_state - 12) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_example_sample(self, iter_size, sample_size, random_state):
        init_random_state = (random_state - 89) % 4235 + 412
        sample_list = [
            {"dist_num": i,
             "data": dist.rvs(size=[iter_size, sample_size], random_state=init_random_state - i)}
            for i, dist in enumerate([self.null_dist,
                                      self.first_dist,
                                      self.second_dist,
                                      self.third_dist])
        ]

        return sample_list

    def get_sample(self, iter_size, sample_size, random_state, y_dist_num=0):
        init_random_state = (random_state - 532) % 4235 + 412
        if y_dist_num == 1:
            y_dist = self.first_dist
        elif y_dist_num == 2:
            y_dist = self.second_dist
        elif y_dist_num == 3:
            y_dist = self.third_dist
        else:
            y_dist = self.null_dist

        x_sample_list = self.null_dist.rvs(size=[iter_size, sample_size], random_state=init_random_state + 1)
        y_sample_list = y_dist.rvs(size=[iter_size, sample_size], random_state=init_random_state - y_dist_num)

        return x_sample_list, y_sample_list

    def get_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        problem_text = r"""
        Перед проведением теста вы хотите убедиться в том,
        что рандомизатор будет работать корректно,
        а именно,
        что сегментатор разбивает выборку на тест и контроль таким образом,
        что распределения параметра $F$ на тесте и контроле совпадают.

        К задаче приложены $4$ файла.
        В каждом файле каждая строка является выборкой,
        количество строк в каждом файле одинаково.
        В первом файле данные из исторического распределения,
        а в остальных файлах данные, изменённые разными способами.

        Ваша задача выбрать {\bf один критерий},
        который позволял бы отличать выборку 
        из исторических данных 
        от выборки из любого другого распределения.
        """ + f"""
        Уровень значимости критерия = {alpha}.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        def solution(x, y):
            res = MMD(compute_kernel="rbf", gamma=1.0).test(x, y)
            return res[1] < alpha

        return solution
