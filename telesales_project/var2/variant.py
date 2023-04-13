from decimal import Decimal
from scipy.stats import ttest_ind
from tools import ProblemVariant, VariantTransformer


telesales_project_variant2 = ProblemVariant(code="telesales_project_var2")


class TransformerTelesalesProjectVariant2(VariantTransformer):
    def __init__(self, code):
        self.code = code
        self.alpha = Decimal("0.05")
        self.beta = Decimal("0.2")
        self.relative_mde = Decimal("0.08")

    def get_alternative(self):
        return "two-sided"

    def get_metric(self):
        return "Флаг продажи"

    def get_description(self, random_state):
        problem_text = f"""
*Контекст*
В связи с постановлением Центрального Банка
наше текущее содержание диалога с клиентом (скрипт)
операторов считается слишком жёстким,
и нам нужно придумать более мягкий скрипт,
который будет всё ещё иметь хорошие показатели.
У нас есть два варианта более мягкого скрипта,
и мы хотим выбрать лучший из них.
При этом у нас нет времени 
чтобы ждать вызревания долгих метрик вроде PV.
        
*Тест*
Мы проводим тест,
в рамках которого мы разбиваем весь поток
на две части рановероятно,
где одной части мы продаём одним вариантом скрипта,
другой - другим.
Целью этого теста
является поиск наилучшего скрипта.

*Статистические вводные*
Уровень значимости {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%}-ное
изменение целевой метрики
с вероятностью {1-self.beta:.0%}.
"""

        return problem_text

    def check_homogeneity(self, x, y):
        return ttest_ind(x, y, equal_var=False, alternative=self.get_alternative()).pvalue
