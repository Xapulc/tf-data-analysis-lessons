import numpy as np

from scipy.stats import norm, expon
from tools import ProblemVariant, VariantTransformer


problem2_variant0 = ProblemVariant(code="stat_task2_var0",
                                   input_data_text="""
                                   Два входных значения.
                                   Первое - уровень доверия, число от $0$ до $1$.
                                   Второе - одномерный массив numpy.ndarray
                                   длин прыжков (в сантиметрах) одного спортсмена.
                                   """,
                                   output_data_text="""
                                   Кортеж или список из двух значений,
                                   равных левой и правой границе доверительного интервала.
                                   """)


class TransformerProblem2Variant0(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def get_sample(self, iter_size, sample_size, random_state):
        a = expon(0.005).rvs(size=iter_size, random_state=42)
        sigma = 10
        eps = norm.rvs(size=[sample_size, iter_size], random_state=42)
        return (eps * sigma + a).T, a

    def get_description(self, random_state):
        problem_text = """
        Школа $N$ имеет сильный состав
        для соревнования в прыжках в длину.
        В ней есть несколько сильных спортсменов,
        но на соревнования нужно отправить одного.
        Тренер Максим вычитал из книги, 
        что длина прыжка имеет нормальное распределение с дисперсией $100$,
        поэтому тренер решил выбрать лучшего школьника
        на основании оценки матожидания длины прыжка.
        Помогите Максиму составить симметричный
        доверительный интервал этой величины
        для каждого студента.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def exact_solution(self, p: float, x: np.array):
        alpha = 1 - p
        return x.mean() - 10 * norm.ppf(1 - alpha / 2) / np.sqrt(len(x)), \
               x.mean() - 10 * norm.ppf(alpha / 2) / np.sqrt(len(x))

    def clt_solution(self, p: float, x: np.array):
        alpha = 1 - p
        return x.mean() - np.sqrt(np.var(x)) * norm.ppf(1 - alpha / 2) / np.sqrt(len(x)), \
               x.mean() - np.sqrt(np.var(x)) * norm.ppf(alpha / 2) / np.sqrt(len(x))
