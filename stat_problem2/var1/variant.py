import numpy as np

from scipy.stats import norm, expon, gamma
from tools import ProblemVariant, VariantTransformer


problem2_variant1 = ProblemVariant(code="stat_task2_var1",
                                   input_data_text="""
                                   Два входных значения.
                                   Первое - уровень доверия, число от $0$ до $1$.
                                   Второе - одномерный массив numpy.ndarray
                                   измерений пути (в метрах) одной модели.
                                   """,
                                   output_data_text="""
                                   Кортеж или список из двух значений,
                                   равных левой и правой границе доверительного интервала.
                                   """)


class TransformerProblem2Variant1(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_t = 2
        max_t = 100
        return min_t + (random_state % (max_t - min_t + 1))

    def get_sample(self, iter_size, sample_size, random_state):
        t = self._get_transformed_random_state(random_state)

        a = expon(0.2).rvs(size=iter_size, random_state=t)
        eps = 0.5 - expon.rvs(size=[sample_size, iter_size], random_state=t)
        return (eps + (t**2) * a / 2).T, a

    def get_description(self, random_state):
        t = self._get_transformed_random_state(random_state)

        problem_text = r"""
        На заводе проводится тестирование модели машины для проверки коэффициента ускорения. 
        В рамках эксперимента выбирается $n$ машин этой модели 
        и измеряется пройденный машиной путь 
        """ + f"через количество секунд, равное {t}." + r"""
        Предполагается, что ошибки измерения пути н.о.р.
        и имеют распределение $1/2 - exp(1)$.
        Постройте симметричный доверительный интервал
        для коэффициента ускорения.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def exact_solution(self, p: float, x: np.array):
        alpha = 1 - p
        return gamma.ppf(alpha / 2, len(x), loc=x.mean() / 50 - 1 / 100, scale=1 / (50 * len(x))), \
               gamma.ppf(1 - alpha / 2, len(x), loc=x.mean() / 50 - 1 / 100, scale=1 / (50 * len(x)))

    def clt_solution(self, p: float, x: np.array):
        alpha = 1 - p
        return x.mean() / 50 + 1 / 100 - np.sqrt(np.var(x)) * norm.ppf(1 - alpha / 2) / (50 * np.sqrt(len(x))), \
               x.mean() / 50 + 1 / 100 - np.sqrt(np.var(x)) * norm.ppf(alpha / 2) / (50 * np.sqrt(len(x)))
