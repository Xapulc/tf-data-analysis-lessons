import numpy as np

from scipy.stats import expon, norm
from tools import ProblemVariant, VariantTransformer


problem1_variant3 = ProblemVariant(code="stat_task1_var3",
                                   input_data_text="""
                                   Одномерный массив numpy.ndarray сумм чеков клиента.
                                   """,
                                   output_data_text="""
                                   Оценка коэффициента $a$.
                                   """)


class TransformerProblem1Variant3(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_shift = 1
        max_shift = 1000
        return min_shift + (random_state % (max_shift - min_shift + 1))

    def get_sample(self, iter_size, sample_size, random_state):
        shift = self._get_transformed_random_state(random_state)

        a = expon(0.5).rvs(size=iter_size, random_state=shift)
        a = np.where(a >= 6, 6, a)
        sigma = expon(0.1).rvs(size=iter_size, random_state=shift)
        eps = norm.rvs(size=[sample_size, iter_size], random_state=shift)
        return (shift + np.exp(eps * sigma + a)).T, a

    def get_description(self, random_state):
        shift = self._get_transformed_random_state(random_state)
        problem_text = f"""Известно, что средний чек клиента имеет
                       распределение ${shift} + """ + r"""\text{LogN}(a, \sigma^2)$,
                       где $\text{LogN}$ - логнормальное распределение.
                       Мы хотим выделить кластер клиентов с наибольшим параметром $a$.
                       Постройте точечную оценку коэффициента $a$."""
        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution_description(self, random_state):
        shift = self._get_transformed_random_state(random_state)

        solution_description = r"""
        Пусть $X_1, \ldots, X_n$ - измерения среднего чека клиентов.
        С распределением из задачи работать неудобно,
        поэтому мы рассмотрим
        $$
        Y_i := \log""" + f"(X_i - {shift})" + r""".
        $$
        В силу условия $Y_i$ н.о.р.
        и $Y_i \sim \mathcal{N}(a, \sigma^2)$.
        Так как матожидание $Y_i$ равно $a$,
        оценкой этого параметра является
        $$
        \overline{Y} = \overline{\log""" + f"(X - {shift})" + r"""}.
        $$
        """

        solution_code = f"`def solution(x):\n" \
                        + f"    return np.log(x - {shift}).mean()`"
        return solution_description, solution_code

    def get_solution(self, random_state):
        shift = self._get_transformed_random_state(random_state)

        def solution(x):
            return np.log(x - shift).mean()

        return solution
