import pandas as pd

from tools import ProblemVariant, VariantTransformer


problem1_variant2 = ProblemVariant(code="stat_task1_var2",
                                   input_data_text="""
                                   Одномерный массив numpy.ndarray
                                   измерений пройденного пути (в м) машин одной модели.
                                   """,
                                   output_data_text="""
                                   Оценка коэффициента ускорения (в м/с^2).
                                   """)


class TransformerProblem1Variant2(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_t = 2
        max_t = 100
        return min_t + (random_state % (max_t - min_t + 1))

    def _get_default_sample(self):
        data = pd.read_csv(self.data_path)
        a_column = "a"

        a_sample = data[a_column]
        data_sample = data.drop(columns=a_column)
        return data_sample, a_sample

    def _get_transformed_random_state(self, random_state):
        min_factor = 1
        max_factor = 50
        return min_factor + (random_state % (max_factor - min_factor + 1))

    def get_score_list(self, random_state):
        return self.default_score_list

    def get_sample(self, random_state):
        data_sample, a_sample = self._get_default_sample()
        exp_deviation = self._get_transformed_random_state(random_state)
        data_sample_transformed = data_sample - exp_deviation
        return data_sample_transformed, a_sample

    def get_description(self, random_state):
        factor = self._get_transformed_random_state(random_state)

        problem_text = f"""
        На заводе проводится тестирование модели машины для проверки коэффициента ускорения. 
        В рамках эксперимента выбирается $n$ машин этой модели 
        и измеряется пройденный машиной путь через количество секунд, равное ${4 * factor}$.
        Предполагается, что ошибки измерения пути н.о.р.
        и имеют распределение Лапласа.
        Постройте точечную оценку коэффициента ускорения.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }
