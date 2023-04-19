from decimal import Decimal
from scipy.stats import gamma
from statsmodels.stats.weightstats import ztest
from tools import ProblemVariant, VariantTransformer

hyp_problem3_variant6 = ProblemVariant(code="hyp_task3_var6",
                                       input_data_text="""
                                       Одна выборка: исторические данные
                                       по затратам на аналогичную подписку.
                                       """,
                                       output_data_text=r"""
                                       bool-значение, ответ на вопрос: 
                                       ''Отклонить ли нулевую гипотезу''
                                       на заданном уровне значимости.
                                       """)


class TransformerHypProblem3Variant6(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

        self.max_cost = 300
        null_gamma_scale = 8
        self.null_dist = gamma(a=self.max_cost / null_gamma_scale, scale=null_gamma_scale)
        self.first_dist = gamma(a=self.max_cost / null_gamma_scale, scale=0.98 * null_gamma_scale)
        gamma_scale = 9
        self.second_dist = gamma(a=self.max_cost / gamma_scale, scale=1.001 * gamma_scale)

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 1
        max_alpha_numerator = 10
        alpha_denominator = 100

        alpha_numerator = min_alpha_numerator + ((random_state - 314) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_example_sample(self, sample_size, random_state):
        init_random_state = (random_state - 521) % 52316
        return self.null_dist.rvs(size=sample_size, random_state=init_random_state % 52316)

    def get_sample(self, iter_size, sample_size, random_state, y_dist_num=0):
        init_random_state = (random_state - 5154) % 52316
        if y_dist_num == 1:
            x_dist = self.first_dist
        elif y_dist_num == 2:
            x_dist = self.second_dist
        else:
            x_dist = self.null_dist

        x_sample_list = x_dist.rvs(size=[iter_size, sample_size], random_state=(init_random_state - y_dist_num) % 52316)
        true_hypothesis = 1 if self.max_cost > x_dist.mean() else 0

        return true_hypothesis, x_sample_list

    def get_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        problem_text = f"""
        Мы хотим запустить новую подписку для клиентов
        с целью увеличения их лояльности.
        Наша цель - не терять на подписке более {self.max_cost} рублей в месяц.

        Имея исторические данные
        о затратах на аналогичную подписку,
        постройте критерий,
        согласно которому можно будет определить,
        что затраты на подписку статзначимо меньше установленного порога.
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
        Здесь нужно было выбрать одновыборочный критерий.
        На лекции был только один одновыборочный критерий,
        его и нужно было использовать: 
        Z-тест на слайде 35 лекции.
        """

        solution_code = f"`def solution(x):\n" \
                        + f"    res = ztest(x1=x, value={self.max_cost}, alternative='smaller')\n" \
                        + f"    return res[1] < {alpha}`"
        return solution_description, solution_code

    def get_solution(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        def solution(x):
            res = ztest(x1=x, value=self.max_cost, alternative="smaller")
            return res[1] < alpha

        return solution
