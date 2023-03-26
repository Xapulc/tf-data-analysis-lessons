from decimal import Decimal
from scipy.stats import expon, gamma, ttest_ind
from tools import ProblemVariant, VariantTransformer

hyp_problem3_variant5 = ProblemVariant(code="hyp_task3_var5",
                                       input_data_text="""
                                       Две выборки показателей NPV:
                                       на контроле и на тесте.
                                       """,
                                       output_data_text=r"""
                                       bool-значение, ответ на вопрос: 
                                       ''Отклонить ли нулевую гипотезу''
                                       на заданном уровне значимости.
                                       """)


class TransformerHypProblem3Variant5(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

        null_mean = 300
        self.null_dist = expon(scale=null_mean)
        self.first_dist = expon(scale=1.3 * null_mean)
        gamma_scale = 80
        self.second_dist = gamma(a=null_mean / gamma_scale, scale=0.8 * gamma_scale)

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 1
        max_alpha_numerator = 10
        alpha_denominator = 100

        alpha_numerator = min_alpha_numerator + ((random_state - 62) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_example_sample(self, sample_size, random_state):
        init_random_state = (random_state - 2362) % 52316
        return self.null_dist.rvs(size=sample_size, random_state=init_random_state)

    def get_sample(self, iter_size, sample_size, random_state, y_dist_num=0):
        init_random_state = (random_state - 743) % 52316
        x_dist = self.null_dist
        if y_dist_num == 1:
            y_dist = self.first_dist
        elif y_dist_num == 2:
            y_dist = self.second_dist
        else:
            y_dist = self.null_dist

        x_sample_list = x_dist.rvs(size=[iter_size, sample_size], random_state=init_random_state + 1)
        y_sample_list = y_dist.rvs(size=[iter_size, sample_size], random_state=init_random_state - y_dist_num)
        true_hypothesis = 1 if x_dist.mean() != y_dist.mean() else 0

        return true_hypothesis, x_sample_list, y_sample_list

    def get_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        problem_text = f"""
        Мы хотим запустить заново закрытый два года назад продукт,
        причём попробовать два тарифа этого продукта.
        Целевой метрикой теста является NPV заявки.

        Для проведения теста мы разделим поток на две части,
        каждой из которых будем предлагать свой тариф.

        Имея исторические данные,
        постройте критерий,
        согласно которому можно будет определить
        статзначимое различие в целевой метрике теста.
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
            res = ttest_ind(x, y, equal_var=False, alternative="two-sided")
            return res.pvalue < alpha

        return solution
