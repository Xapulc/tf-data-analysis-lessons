import pandas as pd

from tools import ProblemVariant, VariantTransformer


problem1_variant0 = ProblemVariant(code="stat_task1_var0",
                                   data_path="stat_problem1/var0/sample.csv",
                                   default_score_list=[{
                                       "sample_size": 1000,
                                       "max_error": 0.01
                                   }, {
                                       "sample_size": 1000,
                                       "max_error": 0.005
                                   }, {
                                       "sample_size": 100,
                                       "max_error": 0.015
                                   }, {
                                       "sample_size": 10,
                                       "max_error": 0.09
                                   }],
                                   input_data_text="""
                                   Одномерный массив numpy.ndarray
                                   длин прыжков (в сантиметрах) одного спортсмена.
                                   """,
                                   output_data_text="""
                                   Оценка матожидания длины прыжка.
                                   """)


class TransformerProblem1Variant0(VariantTransformer):
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
