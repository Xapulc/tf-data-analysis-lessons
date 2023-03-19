import numpy as np

from decimal import Decimal
from scipy.stats import norm, expon, chi2, uniform
from tools import ProblemVariant, VariantTransformer


problem2_variant3 = ProblemVariant(code="stat_task2_var3",
                                   input_data_text="""
                                   Два входных значения.
                                   Первое - уровень доверия, число от $0$ до $1$.
                                   Второе - одномерный массив numpy.ndarray
                                   уровней значимостей.
                                   """,
                                   output_data_text="""
                                   Кортеж или список из двух значений,
                                   равных левой и правой границе доверительного интервала.
                                   """)


class TransformerProblem2Variant3(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 5
        max_alpha_numerator = 100
        alpha_denominator = 1000

        alpha_numerator = min_alpha_numerator + ((random_state - 44) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_sample(self, iter_size, sample_size, random_state):
        min_alpha = self._get_transformed_random_state(random_state)
        min_alpha_random_state = int(1000 * min_alpha)
        float_min_alpha = float(min_alpha)

        max_alpha = uniform.rvs(size=iter_size, random_state=min_alpha_random_state - 12)
        alpha = uniform.rvs(size=[sample_size, iter_size], random_state=min_alpha_random_state)
        return (float_min_alpha + alpha * (max_alpha - float_min_alpha)).T, max_alpha

    def get_description(self, random_state):
        min_alpha = self._get_transformed_random_state(random_state)

        problem_text = f"""
        Пётр пытается понять алгоритм генерации 
        уровня значимости в ДЗ по проверке гипотез.
        Известно, что генерируемый уровень значимости
        имеет равномерное распределение
        $[{min_alpha}, b]$.
        Помогите Петру определить распределение,
        построив доверительный интервал для $b$.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_exact_solution(self, random_state):
        min_alpha = self._get_transformed_random_state(random_state)
        float_min_alpha = float(min_alpha)

        def solution(p, x):
            alpha = 1 - p
            t = x.max() - float_min_alpha
            n = len(x)
            return float_min_alpha + t / ((1 - alpha / 2)**(1 / n)), \
                   float_min_alpha + t / ((alpha / 2)**(1 / n))

        return solution

    def get_clt_solution(self, random_state):
        min_alpha = self._get_transformed_random_state(random_state)
        float_min_alpha = float(min_alpha)

        def solution(p, x):
            alpha = 1 - p
            y = 2 * x - float_min_alpha
            loc = y.mean()
            scale = np.sqrt(y.var() / len(x))
            return max(loc - scale * norm.ppf(1 - alpha / 2), 0), \
                   loc - scale * norm.ppf(alpha / 2)

        return solution
