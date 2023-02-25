from scipy.stats import expon, laplace
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

    def get_sample(self, iter_size, sample_size, random_state):
        t = self._get_transformed_random_state(random_state)

        a = expon(0.2).rvs(size=iter_size, random_state=t)
        eps = laplace.rvs(size=[sample_size, iter_size], random_state=t)
        return (eps + (t**2) * a / 2).T, a

    def get_description(self, random_state):
        t = self._get_transformed_random_state(random_state)

        problem_text = f"""
        На заводе проводится тестирование модели машины для проверки коэффициента ускорения. 
        В рамках эксперимента выбирается $n$ машин этой модели 
        и измеряется пройденный машиной путь через количество секунд, равное ${t}$.
        Предполагается, что ошибки измерения пути н.о.р.
        и имеют распределение Лапласа.
        Постройте точечную оценку коэффициента ускорения.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }
