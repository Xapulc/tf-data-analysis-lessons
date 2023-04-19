import numpy as np

from decimal import Decimal
from scipy.stats import pareto, permutation_test
from tools import ProblemVariant, VariantTransformer

hyp_problem3_variant3 = ProblemVariant(code="hyp_task3_var3",
                                       input_data_text="""
                                       Две выборки показателей NPV:
                                       на контроле и на тесте.
                                       """,
                                       output_data_text=r"""
                                       bool-значение, ответ на вопрос: 
                                       ''Отклонить ли нулевую гипотезу''
                                       на заданном уровне значимости.
                                       """)


class TransformerHypProblem3Variant3(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

        scale = 300
        self.null_dist = pareto(1.1, scale=scale)
        self.first_dist = pareto(1.8, scale=scale)
        self.second_dist = pareto(1.06, loc=-1 * scale, scale=scale)

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 1
        max_alpha_numerator = 10
        alpha_denominator = 100

        alpha_numerator = min_alpha_numerator + ((random_state - 52) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_example_sample(self, sample_size, random_state):
        init_random_state = (random_state - 515) % 52316
        return self.null_dist.rvs(size=sample_size, random_state=init_random_state % 52316)

    def get_sample(self, iter_size, sample_size, random_state, y_dist_num=0):
        init_random_state = (random_state - 5151) % 52316
        x_dist = self.null_dist
        if y_dist_num == 1:
            y_dist = self.first_dist
        elif y_dist_num == 2:
            y_dist = self.second_dist
        else:
            y_dist = self.null_dist

        x_sample_list = x_dist.rvs(size=[iter_size, sample_size], random_state=(init_random_state + 1) % 52316)
        y_sample_list = y_dist.rvs(size=[iter_size, sample_size], random_state=(init_random_state - y_dist_num) % 52316)
        true_hypothesis = 1 if x_dist.mean() > y_dist.mean() else 0

        return true_hypothesis, x_sample_list, y_sample_list

    def get_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        problem_text = f"""
        Поддержка одного из каналов продажи продукта
        несёт для нас большие издержки.
        Мы хотим понять, полезен ли для нас этот канал.
        Целевой метрикой теста является NPV заявки.

        Для проведения теста мы разделим поток на две части,
        одной будем продавать как раньше,
        другой - по-новому, без выбранного канала.

        Имея исторические данные,
        постройте критерий,
        согласно которому можно будет определить
        статзначимое падение целевой метрики на тесте.
        Уровень значимости критерия = {alpha}.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        solution_description = r"""
        Здесь нужно было выбрать двухвыборочный критерий
        исходя из матожидания и дисперсии.
        Пользуясь кодом из лекции 
        (моделирование сходимости выборочных среднего и дисперсии),
        можно заметить, что матожидание конечно,
        а дисперсия бесконечна,
        поэтому из таблицы на слайде 35 лекции следует,
        что подходит перестановочный тест.
        """

        solution_code = f"`def solution(x, y):\n" \
                        + f"    res = permutation_test((x, y),\n" \
                        + f"                           lambda x, y, axis: np.mean(x, axis=axis) - np.mean(y, axis=axis),\n" \
                        + f"                           vectorized=True,\n" \
                        + f"                           n_resamples=1000,\n" \
                        + f"                           alternative='greater',\n" \
                        + f"                           random_state=42)\n" \
                        + f"    return res.pvalue < {alpha}`"
        return solution_description, solution_code

    def get_solution(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        def solution(x, y):
            res = permutation_test((x, y),
                                   lambda x, y, axis: np.mean(x, axis=axis) - np.mean(y, axis=axis),
                                   vectorized=True,
                                   n_resamples=1000,
                                   alternative="greater",
                                   random_state=42)
            return res.pvalue < alpha

        return solution
