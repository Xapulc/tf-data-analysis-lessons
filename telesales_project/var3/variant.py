from decimal import Decimal
from scipy.stats import ttest_ind
from tools import ProblemVariant, VariantTransformer


telesales_project_variant3 = ProblemVariant(code="telesales_project_var3")


class TransformerTelesalesProjectVariant3(VariantTransformer):
    def __init__(self, code):
        self.code = code
        self.alpha = Decimal("0.05")
        self.beta = Decimal("0.1")
        self.relative_mde = Decimal("0.05")

    def get_alternative(self):
        return "greater"

    def get_metric(self):
        return "Расходы"

    def get_description(self, random_state):
        problem_text = f"""
Мы хотим снизить затраты,
и для этого внедряем систему автоматического
дозвона до человека.
Эта система должна сэкономить оператору время,
из-за чего мы сможем платить ему меньше.
В этом тесте мы хотели бы заметить
уменьшение затрат в случае
успешной работы новой системы.

Уровень значимости, как обычно, {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%} целевой метрики
изменение с вероятностью {1-self.beta:.0%}.
"""

        return problem_text

    def check_homogeneity(self, x, y):
        return ttest_ind(x, y, equal_var=False, alternative=self.get_alternative()).pvalue
