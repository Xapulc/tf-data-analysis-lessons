import numpy as np

from decimal import Decimal
from scipy.stats import rv_discrete, anderson_ksamp
from tools import ProblemVariant, VariantTransformer


hyp_problem2_variant1 = ProblemVariant(code="hyp_task2_var1",
                                       input_data_text="""
                                       Две выборки параметра $F$.
                                       """,
                                       output_data_text=r"""
                                       bool-значение, ответ на вопрос: 
                                       "Отклонить ли гипотезу однородности выборок"
                                       на заданном уровне значимости.
                                       """)


class TransformerHypProblem2Variant1(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

        min_value = 18
        max_value = 75
        value_list = np.arange(min_value, max_value + 1)

        p = 1 / value_list
        p = p / p.sum()

        self.null_dist = rv_discrete(name="null", values=(value_list, p))
        self.first_dist = rv_discrete(name="first", values=(value_list + 3, p))

        min_value = 21
        max_value = 75
        value_list = np.arange(min_value, max_value + 1)

        p = 1 / value_list
        p = p / p.sum()
        self.second_dist = rv_discrete(name="second", values=(value_list, p))

        min_value = 18
        max_value = 75
        value_list = np.arange(min_value, max_value + 1)

        p = np.array([2 / i if i < 25 else 1 / i
                      for i in value_list])
        p = p / p.sum()
        self.third_dist = rv_discrete(name="third", values=(value_list, p))

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 1
        max_alpha_numerator = 10
        alpha_denominator = 100

        alpha_numerator = min_alpha_numerator + ((random_state - 37) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_example_sample(self, iter_size, sample_size, random_state):
        init_random_state = (random_state - 14) % 127
        sample_list = [
            {"dist_num": i,
             "data": dist.rvs(size=[iter_size, sample_size], random_state=(init_random_state - i) % 127)}
            for i, dist in enumerate([self.null_dist,
                                      self.first_dist,
                                      self.second_dist,
                                      self.third_dist])
        ]

        return sample_list

    def get_sample(self, iter_size, sample_size, random_state, y_dist_num=0):
        init_random_state = (random_state - 25) % 127
        if y_dist_num == 1:
            y_dist = self.first_dist
        elif y_dist_num == 2:
            y_dist = self.second_dist
        elif y_dist_num == 3:
            y_dist = self.third_dist
        else:
            y_dist = self.null_dist

        x_sample_list = self.null_dist.rvs(size=[iter_size, sample_size], random_state=(init_random_state+1) % 127)
        y_sample_list = y_dist.rvs(size=[iter_size, sample_size], random_state=(init_random_state - y_dist_num) % 127)

        return x_sample_list, y_sample_list

    # def get_sample(self, iter_size, sample_size, random_state):
    #     init_random_state = random_state - 25
    #     dist_list = [
    #         self.null_dist,
    #         self.first_dist,
    #         self.second_dist,
    #         self.third_dist
    #     ]
    #
    #     x_sample = self.null_dist.rvs(size=[iter_size, sample_size], random_state=init_random_state + 1)
    #     y_sample_list = [
    #         dist.rvs(size=[sample_size, iter_size], random_state=init_random_state - i)
    #         for i, dist in enumerate(dist_list)
    #     ]
    #     y_sample_choice_index = randint.rvs(low=0, high=len(dist_list),
    #                                         size=iter_size, random_state=init_random_state + 2)
    #     y_sample = np.choose(y_sample_choice_index, y_sample_list).T
    #
    #     return x_sample, y_sample, y_sample_choice_index

    def get_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        problem_text = r"""
        Перед проведением теста вы хотите убедиться в том,
        что рандомизатор будет работать корректно,
        а именно,
        что сегментатор разбивает выборку на тест и контроль таким образом,
        что распределения параметра $F$ на тесте и контроле совпадают.
        
        К задаче приложены $4$ файла.
        В каждом файле каждая строка является выборкой,
        количество строк в каждом файле одинаково.
        В первом файле данные из исторического распределения,
        а в остальных файлах данные, изменённые разными способами.
        
        Ваша задача выбрать {\bf один критерий},
        который позволял бы отличать выборку 
        из исторических данных 
        от выборки из любого другого распределения.
        """ + f"""
        Уровень значимости критерия = {alpha}.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution_description(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        solution_description = None
        solution_code = f"Общее решение в [Colab](https://colab.research.google.com/drive/1iYevvB2WaE0imsExS5HIdcDILXpAoXir?usp=sharing).\n" \
                        + f"`def solution(x, y):\n" \
                        + f"    res = anderson_ksamp([x, y])\n" \
                        + f"    return res.pvalue < {alpha}`"
        return solution_description, solution_code

    def get_solution(self, random_state):
        alpha = self._get_transformed_random_state(random_state)

        def solution(x, y):
            res = anderson_ksamp([x, y])
            return res.pvalue < alpha

        return solution
