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
*Условие*
Мы хотим сократить заявочную форму 
для оформления кредитной карты 
и ожидаем роста утилизаций.

*Статистические вводные*
Проверка однородности выбранного параметра
осуществяется с уровнем значимости 2%.

Уровень значимости, как обычно, {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%} 
изменение целевой метрики
с вероятностью {1-self.beta:.0%}.
"""

        return problem_text

    def check_homogeneity(self, x, y):
        return ttest_ind(x, y, equal_var=False, alternative=self.get_alternative()).pvalue
