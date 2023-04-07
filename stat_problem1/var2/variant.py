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

    def get_solution_description(self, random_state):
        t = self._get_transformed_random_state(random_state)

        return r"""
        Пусть $X_1, \ldots, X_n$ - измерения длины пройденного пути,
        $\varepsilon_1, \ldots, \varepsilon_n 
        \sim \text{Laplace}$ - ошибки измерений.
        Тогда
        $$
        X_i = \frac{a """ + f"{t}" + r"""^2}{2} + \varepsilon_i,
        $$
        где $a$ -- коэффициент ускорения.
        Используем метод из лекции,
        связав матожидание измерения длины пройденного пути 
        с оцениваемым параметром.
        Имеем
        $$
        \mathbb{E} X_1 = """ + f"{(t**2) / 2} a" + r""" + \mathbb{E} \varepsilon_i
        = """ + f"{(t**2) / 2} a." + r"""
        $$
        Таким образом, $\mathbb{E} X_1 = g(a)$,
        где
        $$
        g(a) = """ + f"{(t**2) / 2} a" + r""",
        g^{-1}(x) = \frac{x}{""" + f"{(t**2) / 2}" + r"""}.
        $$
        Отсюда в силу утверждения из лекции
        $$
        g^{-1}(\overline{X})
        = \frac{\overline{X}}{""" + f"{(t**2) / 2}" + r"""}.
        \to a.
        $$
        """

    def get_solution(self, random_state):
        t = self._get_transformed_random_state(random_state)

        def solution(x):
            return 2 * x.mean() / (t**2)

        return solution
