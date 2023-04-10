from decimal import Decimal
from scipy.stats import ttest_ind
from tools import ProblemVariant, VariantTransformer


telesales_project_variant1 = ProblemVariant(code="telesales_project_var1")


class TransformerTelesalesProjectVariant1(VariantTransformer):
    def __init__(self, code):
        self.code = code
        self.alpha = Decimal("0.05")
        self.beta = Decimal("0.2")
        self.relative_mde = Decimal("0.05")

    def get_alternative(self):
        return "less"

    def get_metric(self):
        return "NPV"

    def get_description(self, random_state):
        problem_text = f"""
*Условие*
Мы хотим попробовать уменьшить цену продукта,
ожидая увеличения доходности
с одного задания на обзвон.

*Статистические вводные*
Уровень значимости, как обычно, {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%} 
изменение целевой метрики
с вероятностью {1-self.beta:.0%}.
"""

        return problem_text

    def check_homogeneity(self, x, y):
        return ttest_ind(x, y, equal_var=False, alternative=self.get_alternative()).pvalue
