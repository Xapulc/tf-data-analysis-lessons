import numpy as np

from decimal import Decimal
from scipy.stats import bernoulli, norm
from tools import ProblemVariant, VariantTransformer


unbalanced_sample_variant3 = ProblemVariant(code="unbalanced_sample_var3")


class UnbalancedSampleVariant3(VariantTransformer):
    def __init__(self, code):
        self.code = code
        self.alpha = Decimal("0.05")
        self.beta = Decimal("0.1")
        self.relative_mde = Decimal("0.05")
        self.days_cnt = 28
        self.total_days_cnt = 14
        self.dau = 20000

    def _get_transformed_random_state(self, random_state):
        min_num = 6
        max_num = 30
        return (min_num + (random_state % (max_num - min_num + 1))) / 100

    def get_sample(self, random_state):
        p = self._get_transformed_random_state(random_state)
        return bernoulli(p).rvs(size=self.days_cnt * self.dau)

    def get_description(self, random_state):
        problem_text = f"""
*Контекст*
Организация работы с операторами
дорога и сложна.
Мы хотим попробовать внедрить
продажные звонки роботом,
притом так,
чтобы он продавал лучше операторов.

*Тест*
Небольшую часть потока заданий
мы хотим перевести на продажного робота.
В этом тесте мы хотим сделать вывод о том,
кто лучше - оператор или робот.

*Данные*
Результаты заданий (продали продукт или нет)
за последние {self.days_cnt} дней
приведены в файле,
присылаемом вместе с заданием.

*Статистические вводные*
Уровень значимости {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%}-ное
изменение целевой метрики
с вероятностью {1 - self.beta:.0%}.

*Задача*
Нам нужно понять,
какую максимальную долю заданий можно оставить операторам,
учитывая,
что тест мы хотим завершить за {self.total_days_cnt} дней.
"""

        return problem_text

    def get_solution_description(self, random_state):
        sample = self.get_sample(random_state)
        mu = sample.mean()
        sigma_sqr = sample.var()
        sample_size = self.total_days_cnt * len(sample) / self.days_cnt
        mde = mu * float(self.relative_mde)

        c = sigma_sqr * ((norm.ppf(1 - float(self.alpha / 2)) - norm.ppf(float(self.beta))) ** 2) \
            / (sample_size * (mde ** 2))
        gamma = 0.5 + np.sqrt(0.25 - c)

        return f"""
*Данные*
Общий размер выборки (L): {sample_size}
Выборочное среднее (m): {mu:.3f}
Выборочная дисперсия (s): {sigma_sqr:.3f}
MDE (d): {mde:.3f}

*Решение*
Так как
L = n + m
= s^2 (z(1-a/2) - z(b))^2 / (g (1-g) d^2),
где z - квантиль нормального, g - доля теста, то
g (1-g) = s^2 (z(1-a/2) - z(b))^2 (L d^2) =: c.
Решая квадратное уравнение, получаем
g = 0.5 + (0.25 - c)^(1/2).
В нашем случае c = {c:.5f},
откуда g = {gamma:.3f}.
"""
