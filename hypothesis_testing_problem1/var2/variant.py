import numpy as np

from decimal import Decimal
from scipy.stats import binom
from statsmodels.stats.proportion import proportions_ztest
from tools import ProblemVariant, VariantTransformer


hyp_problem1_variant2 = ProblemVariant(code="hyp_task1_var2",
                                       input_data_text="""
                                       Четыре целых числа:
                                       количество продаж на контроле,
                                       количество заявок на контроле,
                                       количество продаж на тесте
                                       и количество заявок на тесте.
                                       """,
                                       output_data_text="""
                                       bool-значение, ответ на вопрос: "Отклонить ли нулевую гипотезу?".
                                       """)


class TransformerHypProblem1Variant2(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

        self.initial_p = Decimal("0.4")
        self.positive_delta_p = Decimal("0.1")
        self.negative_delta_p = Decimal("0.1")

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 1
        max_alpha_numerator = 10
        alpha_denominator = 100

        alpha_numerator = min_alpha_numerator + ((random_state - 1) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_sample(self, iter_size, sample_size, random_state, delta_factor=0):
        transformed_random_state = (random_state - 423) % 4512
        control_p = self.initial_p
        if delta_factor > 0:
            delta = self.initial_p * self.positive_delta_p * delta_factor
        elif delta_factor < 0:
            delta = self.initial_p * self.negative_delta_p * delta_factor
        else:
            delta = 0

        test_p = self.initial_p * Decimal("1") + delta
        true_hypothesis = 1 if test_p != control_p else 0

        control_sample = binom.rvs(n=sample_size, p=float(control_p), size=iter_size,
                                   random_state=transformed_random_state % 4512)
        test_sample = binom.rvs(n=sample_size, p=float(test_p), size=iter_size,
                                random_state=(transformed_random_state - 1) % 4512)

        control_size = sample_size * np.ones(iter_size)
        test_size = sample_size * np.ones(iter_size)
        return true_hypothesis, control_p, control_sample, control_size, test_p, test_sample, test_size

    def get_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        problem_text = f"""
        Мы запускаем новый продукт,
        в рамках которого 
        мы хотим проверить два способа продажи клиенту
        и выяснить какой из них лучше.
        Составьте критерий
        с уровнем значимости ${alpha}$,
        который позволит по данным теста
        принять решение о лучшем способе продажи.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        solution_description = r"""
        Здесь нам нужно определить 
        наилучшую стратегию продажи.
        В этом случае $H_0: p_c = p_t$, $H_1: p_c \neq p_t$,
        где $p_c$ - конверсия на контроле,
        $p_t$ - конверсия на тесте.
        
        Для проверки гипотезы равенства конверсий
        используется Z-тест.
        """

        solution_code = f"`def solution(x_success, x_cnt, y_success, y_cnt):\n" \
                        + f"    res = proportions_ztest([x_success, y_success],\n" \
                        + f"                            [x_cnt, y_cnt],\n" \
                        + f"                            alternative='two-sided')\n" \
                        + f"    return res[1] < {alpha}`"
        return solution_description, solution_code

    def get_solution(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        def solution(x_success, x_cnt, y_success, y_cnt):
            res = proportions_ztest([x_success, y_success],
                                    [x_cnt, y_cnt],
                                    alternative="two-sided")
            return res[1] < alpha

        return solution
