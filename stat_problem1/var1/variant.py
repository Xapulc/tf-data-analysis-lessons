import pandas as pd

from tools import ProblemVariant, VariantTransformer


problem1_variant1 = ProblemVariant(code="stat_task1_var1",
                                   data_path="stat_problem1/var1/sample.csv",
                                   default_score_list=[{
                                       "sample_size": 1000,
                                       "max_error": 0.001
                                   }, {
                                       "sample_size": 1000,
                                       "max_error": 0.0001
                                   }, {
                                       "sample_size": 100,
                                       "max_error": 0.00015
                                   }, {
                                       "sample_size": 10,
                                       "max_error": 0.0011
                                   }],
                                   input_data_text="""
                                   Одномерный массив numpy.ndarray
                                   измерений скорости (в м/c) машин одной модели.
                                   """,
                                   output_data_text="""
                                   Оценка коэффициента ускорения (в м/с^2).
                                   """)


class TransformerProblem1Variant1(VariantTransformer):
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

    def _get_transformed_random_state(self, random_state):
        min_exp_deviation = -1
        max_exp_deviation = 50
        return min_exp_deviation + (random_state % (max_exp_deviation - min_exp_deviation + 1))

    def get_score_list(self, random_state):
        return self.default_score_list

    def get_sample(self, random_state):
        data_sample, a_sample = self._get_default_sample()
        exp_deviation = self._get_transformed_random_state(random_state)
        data_sample_transformed = data_sample - exp_deviation
        return data_sample_transformed, a_sample

    def get_description(self, random_state):
        exp_deviation = self._get_transformed_random_state(random_state)

        problem_text = f"""
        На заводе проводится тестирование модели машины для проверки коэффициента ускорения. 
        В рамках эксперимента выбирается $n$ машин этой модели 
        и измеряется скорость машины через $10$ секунд.
        Предполагается, что ошибки измерения скорости н.о.р.
        и имеют распределение ${-2-exp_deviation} + exp(1)$.
        Постройте точечную оценку коэффициента ускорения.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }
