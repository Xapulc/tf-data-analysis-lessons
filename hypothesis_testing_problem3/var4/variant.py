from decimal import Decimal
from scipy.stats import cauchy, mannwhitneyu
from tools import ProblemVariant, VariantTransformer

hyp_problem3_variant4 = ProblemVariant(code="hyp_task3_var4",
                                       input_data_text="""
                                       Две выборки показателей NPV:
                                       на контроле и на тесте.
                                       """,
                                       output_data_text=r"""
                                       bool-значение, ответ на вопрос: 
                                       ''Отклонить ли нулевую гипотезу''
                                       на заданном уровне значимости.
                                       """)


class TransformerHypProblem3Variant4(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

        scale = 300
        self.null_dist = cauchy(1 * scale)
        self.first_dist = cauchy(1.0017 * scale)
        self.second_dist = cauchy(0.9997 * scale)

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 1
        max_alpha_numerator = 10
        alpha_denominator = 100

        alpha_numerator = min_alpha_numerator + ((random_state - 523) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_example_sample(self, sample_size, random_state):
        init_random_state = (random_state - 754) % 52316
        return self.null_dist.rvs(size=sample_size, random_state=init_random_state % 52316)

    def get_sample(self, iter_size, sample_size, random_state, y_dist_num=0):
        init_random_state = (random_state - 856) % 52316
        x_dist = self.null_dist
        if y_dist_num == 1:
            y_dist = self.first_dist
        elif y_dist_num == 2:
            y_dist = self.second_dist
        else:
            y_dist = self.null_dist

        x_sample_list = x_dist.rvs(size=[iter_size, sample_size], random_state=(init_random_state + 1) % 52316)
        y_sample_list = y_dist.rvs(size=[iter_size, sample_size], random_state=(init_random_state - y_dist_num) % 52316)
        true_hypothesis = 1 if x_dist.median() < y_dist.median() else 0

        return true_hypothesis, x_sample_list, y_sample_list

    def get_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        problem_text = f"""
        Мы хотим протестировать новую фичу в мобильном приложении
        и надеемся, что она увеличит транзакционную активность лояльных клиентов.
        Целевой метрикой теста является сумма транзакций клиента за месяц.

        Для проведения теста мы разделим поток на две части,
        у одной мобильное приложение будет без новой фичи,
        у другой - с новой фичей.

        Имея исторические данные,
        постройте критерий,
        согласно которому можно будет определить
        статзначимое увеличение целевой метрики на тесте.
        Уровень значимости критерия = {alpha}.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        def solution(x, y):
            res = mannwhitneyu(x, y, alternative="less")
            return res.pvalue < alpha

        return solution
