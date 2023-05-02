import numpy as np

from decimal import Decimal
from scipy.stats import bernoulli, norm
from tools import ProblemVariant, VariantTransformer


unbalanced_sample_variant2 = ProblemVariant(code="unbalanced_sample_var2")


class UnbalancedSampleVariant2(VariantTransformer):
    def __init__(self, code):
        self.code = code
        self.alpha = Decimal("0.03")
        self.beta = Decimal("0.1")
        self.relative_mde = Decimal("0.1")
        self.days_cnt = 7
        self.dau = 150000

    def _get_transformed_random_state(self, random_state):
        min_num = 5
        max_num = 20
        return (min_num + (random_state % (max_num - min_num + 1))) / 100

    def get_sample(self, random_state):
        p = self._get_transformed_random_state(random_state)
        return bernoulli(p).rvs(size=50000)

    def get_description(self, random_state):
        problem_text = f"""
*Контекст*
Мы хотим встроить в экран платежа 
нашу новую услугу.
Наши коллеги с команды платежей переживают,
что наша доработка
снизит конверсию экрана платежа.

*Тест*
Мы хотим провести тест, 
где на небольшую часть клиентов раскатим 
экран платежей с нашей услугой,
а остальной части клиентов
будем показывать старую версию экрана.
При этом мы хотим провести тест за {self.days_cnt} дней.

*Данные*
Через экран платежей в среднем проходят {self.dau} людей в день.
Статистика совершения платежей в МП
приведена в файле, приложенном к задаче.

*Статистические вводные*
Уровень значимости {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%}-ное
изменение целевой метрики
с вероятностью {1 - self.beta:.0%}.

*Задача*
Нам нужно понять,
какую минимальную долю людей можно отправлять в тест,
учитывая сроки проведения теста.
"""

        return problem_text

    def get_solution_description(self, random_state):
        sample = self.get_sample(random_state)
        mu = sample.mean()
        sigma_sqr = sample.var()
        sample_size = self.days_cnt * self.dau
        mde = mu * float(self.relative_mde)

        c = sigma_sqr * ((norm.ppf(1 - float(self.alpha)) - norm.ppf(float(self.beta))) ** 2) \
            / (sample_size * (mde ** 2))
        gamma = 0.5 - np.sqrt(0.25 - c)

        return f"""
*Данные*
Общий размер выборки (L): {sample_size}
Выборочное среднее (m): {mu:.3f}
Выборочная дисперсия (s): {sigma_sqr:.3f}
MDE (d): {mde:.3f}

*Решение*
Так как
L = n + m
= s^2 (z(1-a) - z(b))^2 / (g (1-g) d^2),
где z - квантиль нормального, g - доля теста, то
g (1-g) = s^2 (z(1-a) - z(b))^2 (L d^2) =: c.
Решая квадратное уравнение, получаем
g = 0.5 - (0.25 - c)^(1/2).
В нашем случае c = {c:.5f},
откуда g = {gamma:.3f}.
"""
