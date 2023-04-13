from decimal import Decimal
from scipy.stats import ttest_ind
from tools import ProblemVariant, VariantTransformer


credit_card_project_variant1 = ProblemVariant(code="credit_card_project_var1")


class TransformerCreditCardProjectVariant1(VariantTransformer):
    def __init__(self, code):
        self.code = code
        self.alpha = Decimal("0.05")
        self.beta = Decimal("0.05")
        self.relative_mde = Decimal("0.03")

    def get_alternative(self):
        return "less"

    def get_metric(self):
        return "Флаг утилизации счёта"

    def get_description(self, random_state):
        problem_text = f"""
*Контекст*
Мы провели Cust Dev,
и поняли,
что форма авторизации для клиента сложна,
и из-за этого часть клиентов
отваливается в заявочном процессе.
Мы решили разработать
новый процесс авторизации,
и у нас есть гипотеза,
что он позволит повысить
утилизации наших счетов.
        
*Тест*
Мы проводим тест,
в рамках которого мы разбиваем весь поток
на две части рановероятно,
где у одной части (контроля) 
старый процесс авторизации,
а у второй части (теста) - новый.
Целью этого теста
является повышение утилизаций счёта.

*Статистические вводные*
Проверка однородности выбранного параметра
осуществяется с уровнем значимости 2%.

Уровень значимости {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%}-ное
изменение целевой метрики
с вероятностью {1-self.beta:.0%}.
"""

        return problem_text

    def check_homogeneity(self, x, y):
        return ttest_ind(x, y, equal_var=False, alternative=self.get_alternative()).pvalue
