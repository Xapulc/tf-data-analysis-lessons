import numpy as np

from scipy.stats import expon, poisson
from tools import ProblemVariant, VariantTransformer


problem1_variant4 = ProblemVariant(code="stat_task1_var4",
                                   input_data_text="""
                                   Одномерный массив numpy.ndarray количества ламп,
                                   поставленных в каждую из компаний-партнёров.
                                   """,
                                   output_data_text=r"""
                                   Оценка коэффициента $\lambda$.
                                   """)


class TransformerProblem1Variant4(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_t = 1
        max_t = 90
        return min_t + (random_state % (max_t - min_t + 1))

    def get_sample(self, iter_size, sample_size, random_state):
        t = self._get_transformed_random_state(random_state)

        lmbda = expon(0.1).rvs(size=iter_size, random_state=t)
        k = poisson.rvs(mu=lmbda * t, size=[sample_size, iter_size], random_state=t+1)
        return k.T, lmbda

    def get_description(self, random_state):
        t = self._get_transformed_random_state(random_state)

        problem_text = f"""Производитель ламп $M$ хочет оценить 
                       эффективность своей продукции.
                       Для этого он рассматривает
                       поставки в компании-партнёры за количество дней,
                       равное {t}.""" + r"""
                       Известно, что при интенсивности $\lambda$ выгорания ламп
                       за $t$ дней количество поставок в компанию-партнёр
                       имеет распределение Пуассона с параметром $\lambda t$.
                       Оцените параметр $\lambda$ по размерам поставок
                       в $n$ компаний-партнёров.
                       """
        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution_description(self, random_state):
        t = self._get_transformed_random_state(random_state)

        solution_description = r"""
        Пусть $X_1, \ldots, X_n$ - количества поставок в компании-партнёры.
        Тогда $X_i \sim \text{Poisson}(""" + f"{t}" + r""" \lambda)$.
        
        Используем метод из лекции,
        связав матожидание количества поставок
        с оцениваемым параметром.
        Имеем
        $$
        \mathbb{E} X_1 = """ + f"{t}" + r""" \lambda.
        $$
        Таким образом, $\mathbb{E} X_1 = g(\lambda)$,
        где
        $$
        g(\lambda) = """ + f"{t}" + r""" \lambda,
        g^{-1}(x) = \frac{x}{""" + f"{t}" + r"""}.
        $$
        Отсюда в силу утверждения из лекции
        $$
        g^{-1}(\overline{X})
        = \frac{\overline{X}}{""" + f"{t}" + r"""}.
        \to a.
        $$
        """

        solution_code = f"`def solution(x):\n" \
                        + f"    return x.mean() / {t}`"
        return solution_description, solution_code

    def get_solution(self, random_state):
        t = self._get_transformed_random_state(random_state)

        def solution(x):
            return x.mean() / t

        return solution
