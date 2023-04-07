import numpy as np

from decimal import Decimal
from scipy.stats import binom
from statsmodels.stats.proportion import proportions_ztest
from tools import ProblemVariant, VariantTransformer


hyp_problem1_variant3 = ProblemVariant(code="hyp_task1_var3",
                                       input_data_text="""
                                       Четыре целых числа:
                                       количество продаж на контроле,
                                       количество заявок на контроле,
                                       количество продаж на тесте
                                       и количество заявок на тесте.
                                       """,
                                       output_data_text="""
                                       bool-значение, ответ на вопрос: "Отклонить ли гипотезу?".
                                       """)


class TransformerHypProblem1Variant3(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

        self.initial_p = Decimal("0.14")
        self.positive_delta_p = Decimal("0.03")
        self.negative_delta_p = Decimal("0.25")

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 1
        max_alpha_numerator = 10
        alpha_denominator = 100

        alpha_numerator = min_alpha_numerator + ((random_state - 3) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_sample(self, iter_size, sample_size, random_state, delta_factor=0):
        transformed_random_state = (random_state - 451) % 4512 + 4124

        control_p = self.initial_p
        if delta_factor > 0:
            delta = self.initial_p * self.positive_delta_p * delta_factor
        elif delta_factor < 0:
            delta = self.initial_p * self.negative_delta_p * delta_factor
        else:
            delta = 0

        test_p = self.initial_p * Decimal("1") + delta
        true_hypothesis = 1 if test_p < control_p else 0

        control_sample = binom.rvs(n=sample_size, p=float(control_p), size=iter_size,
                                   random_state=transformed_random_state)
        test_sample = binom.rvs(n=sample_size, p=float(test_p), size=iter_size,
                                random_state=transformed_random_state - 1)

        control_size = sample_size * np.ones(iter_size)
        test_size = sample_size * np.ones(iter_size)
        return true_hypothesis, control_p, control_sample, control_size, test_p, test_sample, test_size

    def get_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        problem_text = f"""
        Поддержка одного из каналов продажи несёт
        для нас большие издержки.
        Мы хотим понять, 
        можно ли отключить этот канал 
        и не потерять в продажах.
        Составьте критерий
        с уровнем значимости ${alpha}$,
        который позволит по данным теста
        принять решение об отключении выбранного канала продажи.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        def solution(x_success, x_cnt, y_success, y_cnt):
            res = proportions_ztest([x_success, y_success],
                                    [x_cnt, y_cnt],
                                    alternative="larger")
            return res[1] < alpha

        return solution
