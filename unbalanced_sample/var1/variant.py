import numpy as np

from decimal import Decimal
from scipy.stats import binom, norm
from tools import ProblemVariant, VariantTransformer


unbalanced_sample_variant1 = ProblemVariant(code="unbalanced_sample_var1")


class UnbalancedSampleVariant1(VariantTransformer):
    def __init__(self, code):
        self.code = code
        self.alpha = Decimal("0.05")
        self.beta = Decimal("0.2")
        self.relative_mde = Decimal("0.05")
        self.days_cnt = 14

    def _get_transformed_random_state(self, random_state):
        min_num = 1
        max_num = 10
        return (min_num + (random_state % (max_num - min_num + 1))) / 100

    def get_sample(self, random_state):
        p = self._get_transformed_random_state(random_state)
        return binom(self.days_cnt, p).rvs(size=300000)

    def get_description(self, random_state):
        problem_text = f"""
*Контекст*
Нам кажется, что в текущем виде
у клиента мало инструментов
для анализа своих финансовых активов.
Мы хотим попробовать добавить в мобильное приложение
аналитику по тратам клиента.

*Тест*
Мы не знаем, зайдёт ли клиентам MVP такого функционала,
поэтому хотим провести тест, где небольшой части клиентов
мы включим новый функционал,
а другой - оставим текущий интерфейс.
Поговорив с коллегами,
мы решили,
что целевой метрикой теста
будет количество дней с заходами в МП
среди первых {self.days_cnt} дней теста.

*Данные*
По текущей базе клиентов мы собрали статистику использования МП,
которая приложена к задаче.

*Статистические вводные*
Уровень значимости {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%}-ное
изменение целевой метрики
с вероятностью {1 - self.beta:.0%}.

*Задача*
Нам нужно понять,
какую минимальную долю людей мы можем отправить в тест,
чтобы получить статзначимый результат.
"""

        return problem_text

    def get_solution_description(self, random_state):
        sample = self.get_sample(random_state)
        mu = sample.mean()
        sigma_sqr = sample.var()
        sample_size = len(sample)
        mde = mu * float(self.relative_mde)

        c = sigma_sqr * ((norm.ppf(1 - float(self.alpha)) - norm.ppf(float(self.beta)))**2) \
            / (sample_size * (mde**2))
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
