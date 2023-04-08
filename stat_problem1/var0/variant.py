from scipy.stats import norm, expon
from tools import ProblemVariant, VariantTransformer


problem1_variant0 = ProblemVariant(code="stat_task1_var0",
                                   input_data_text="""
                                   Одномерный массив numpy.ndarray
                                   длин прыжков (в сантиметрах) одного спортсмена.
                                   """,
                                   output_data_text="""
                                   Оценка матожидания длины прыжка.
                                   """)


class TransformerProblem1Variant0(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def get_sample(self, iter_size, sample_size, random_state):
        a = 200 + expon(0.01).rvs(size=iter_size, random_state=42)
        eps = norm.rvs(size=[sample_size, iter_size], random_state=42)
        return (eps + a).T, a

    def get_description(self, random_state):
        problem_text = """
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

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution_description(self, random_state):
        return r"""
        Лучшая оценка среднего нормального - среднее.
        Отсюда получаем
        $$
        \widehat{a} := \overline{l}.
        $$
        Эта оценка
        \begin{enumerate}
        \item несмещённая;
        \item состоятельная;
        \item асимптотически нормальная.
        \end{enumerate}
        """

    def get_solution(self, random_state):
        def solution(x):
            return x.mean()

        return solution
