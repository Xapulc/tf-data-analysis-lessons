import pandas as pd

from tools import ProblemVariant, VariantTransformer


problem2_variant0 = ProblemVariant(code="stat_task2_var0",
                                   data_path="stat_problem2/var0/sample.csv",
                                   default_score_list=[{
                                       "sample_size": 1000,
                                       "confidence": 0.99,
                                       "max_error": 0.02,
                                       "max_interval_length": 2
                                   }, {
                                       "sample_size": 1000,
                                       "confidence": 0.9,
                                       "max_error": 0.12,
                                       "max_interval_length": 1.1
                                   }, {
                                       "sample_size": 100,
                                       "confidence": 0.7,
                                       "max_error": 0.32,
                                       "max_interval_length": 2.2
                                   }, {
                                       "sample_size": 100,
                                       "confidence": 0.9,
                                       "max_error": 0.11,
                                       "max_interval_length": 3.3
                                   }, {
                                       "sample_size": 10,
                                       "confidence": 0.95,
                                       "max_error": 0.1,
                                       "max_interval_length": 13
                                   }, {
                                       "sample_size": 10,
                                       "confidence": 0.9,
                                       "max_error": 0.11,
                                       "max_interval_length": 10.6
                                   }],
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
    def __init__(self, code, data_path, default_score_list, input_data_text, output_data_text):
        self.code = code
        self.data_path = data_path
        self.default_score_list = default_score_list
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_default_sample(self):
        data = pd.read_csv(self.data_path)
        a_column = "a"

        a_sample = data[a_column]
        data_sample = data.drop(columns=a_column)
        return data_sample, a_sample

    def get_score_list(self, random_state):
        return self.default_score_list

    def get_sample(self, random_state):
        return self._get_default_sample()

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
