from scipy.stats import expon
from tools import ProblemVariant, VariantTransformer


problem1_variant1 = ProblemVariant(code="stat_task1_var1",
                                   input_data_text="""
                                   Одномерный массив numpy.ndarray
                                   измерений скорости (в м/c) машин одной модели.
                                   """,
                                   output_data_text="""
                                   Оценка коэффициента ускорения (в м/с^2).
                                   """)


class TransformerProblem1Variant1(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_exp_deviation = 1
        max_exp_deviation = 50
        return min_exp_deviation + (random_state % (max_exp_deviation - min_exp_deviation + 1))

    def get_sample(self, iter_size, sample_size, random_state):
        t = 10
        exp_deviation = self._get_transformed_random_state(random_state)

        a = expon(0.3).rvs(size=iter_size, random_state=exp_deviation)
        eps = expon.rvs(size=[sample_size, iter_size], random_state=exp_deviation) - exp_deviation
        return (eps + t * a).T, a

    def get_description(self, random_state):
        exp_deviation = self._get_transformed_random_state(random_state)

        problem_text = f"""
        На заводе проводится тестирование модели машины для проверки коэффициента ускорения. 
        В рамках эксперимента выбирается $n$ машин этой модели 
        и измеряется скорость машины через $10$ секунд.
        Предполагается, что ошибки измерения скорости н.о.р.
        и имеют распределение ${-exp_deviation} + exp(1)$.
        Постройте точечную оценку коэффициента ускорения.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution(self, random_state):
        exp_deviation = self._get_transformed_random_state(random_state)

        def solution(x):
            return (x.mean() + exp_deviation - 1) / 10

        return solution
