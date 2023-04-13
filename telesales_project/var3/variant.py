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
*Контекст*
Мы много платим оператору из-за того,
что он сам по каждому заданию
звонит клиенту и ждёт ответа клиента.
Мы хотим попробовать снизить затраты на операторов,
внедрив систему,
которая будет сама звонить человеку
и в случае успеха перенаправлять задание оператору.
        
*Тест*
Мы проводим тест,
в рамках которого мы разбиваем весь поток
на две части рановероятно,
где одной части (контролю) мы продаём 
без автоматической системы дозвона,
а второй части (тесту) - с ней.
Целью этого теста
является снижение расходов на задание.

*Статистические вводные*
Уровень значимости {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%}-ное 
изменение целевой метрики
с вероятностью {1-self.beta:.0%}.
"""

        return problem_text

    def check_homogeneity(self, x, y):
        return ttest_ind(x, y, equal_var=False, alternative=self.get_alternative()).pvalue
