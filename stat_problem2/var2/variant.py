import numpy as np

from scipy.stats import norm, expon, chi2
from tools import ProblemVariant, VariantTransformer


problem2_variant2 = ProblemVariant(code="stat_task2_var2",
                                   input_data_text="""
                                   Два входных значения.
                                   Первое - уровень доверия, число от $0$ до $1$.
                                   Второе - одномерный массив numpy.ndarray
                                   расстояний от места попадания стрелы до центра мишени (в сантиметрах).
                                   """,
                                   output_data_text="""
                                   Кортеж или список из двух значений,
                                   равных левой и правой границе доверительного интервала.
                                   """)


class TransformerProblem2Variant2(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_factor = 2
        max_factor = 50
        return min_factor + (random_state % (max_factor - min_factor + 1))

    def get_sample(self, iter_size, sample_size, random_state):
        factor = self._get_transformed_random_state(random_state)

        sigma = expon(0.5).rvs(size=iter_size, random_state=factor)
        x = norm.rvs(size=[sample_size, iter_size], random_state=factor)
        y = norm.rvs(size=[sample_size, iter_size], random_state=factor+1)

        return np.sqrt(factor * (((x * sigma)**2) + ((y * sigma)**2)).T), sigma

    def get_description(self, random_state):
        factor = self._get_transformed_random_state(random_state)

        problem_text = r"""
        Иван является профессионалом в стрельбе из лука.
        Можно предполагать, что в ортонормированной системе координат
        с центром в центре мишени координаты $(X, Y)$
        места попадания стрелы независимы
        и имеют распределение $\mathcal{N}(0, """ + str(factor) + r""" \sigma^2)$.
        Иван выпускает $n$ стрел и считает расстояния до центра мишени.
        Помогите Ивану определить свой профессионализм,
        построив симметричный доверительный интервал для параметра $\sigma$.
        {\it Указание}: если $X \sim \mathcal{N}(0, 1)$,
        то $X^2$ имеет распределение хи-квадрат
        со степенью свободы $1$.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_exact_solution(self, random_state):
        factor = self._get_transformed_random_state(random_state)

        def solution(p, x):
            alpha = 1 - p
            scale = (x**2).sum() / factor
            return np.sqrt(scale / chi2.ppf(1 - alpha / 2, 2 * len(x))), \
                   np.sqrt(scale / chi2.ppf(alpha / 2, 2 * len(x)))

        return solution

    def get_clt_solution(self, random_state):
        factor = self._get_transformed_random_state(random_state)

        def solution(p, x):
            alpha = 1 - p
            loc = (x**2).mean()
            scale = np.sqrt(np.var(x**2)) / np.sqrt(len(x))
            return np.sqrt(max((loc - scale * norm.ppf(1 - alpha / 2)) / (2 * factor), 0)), \
                   np.sqrt((loc - scale * norm.ppf(alpha / 2)) / (2 * factor))

        return solution
