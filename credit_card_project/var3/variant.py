from decimal import Decimal
from scipy.stats import ttest_ind
from tools import ProblemVariant, VariantTransformer


credit_card_project_variant3 = ProblemVariant(code="credit_card_project_var3")


class TransformerCreditCardProjectVariant3(VariantTransformer):
    def __init__(self, code):
        self.code = code
        self.alpha = Decimal("0.05")
        self.beta = Decimal("0.15")
        self.relative_mde = Decimal("0.2")

    def get_alternative(self):
        return "less"

    def get_metric(self):
        return "NPV"

    def get_description(self, random_state):
        problem_text = f"""
*Контекст*
ЦБ смягчило правило,
ограничивающее варианты продажи услуги.
Мы хотим попробовать
более агрессивную продажу услуги,
но боимся,
что это повлияет на экономику основного продукта (КК)
из-за негатива клиентов.

*Тест*
Мы проводим тест,
в рамках которого мы разбиваем весь поток
на две части рановероятно,
где одной части (контролю) 
мы будем предлагать услугу текущим способом,
а второй части (тесту) 
- новым более агрессивным способом.
Целью этого теста 
является увеличение доходности КК + услуги.

*Статистические вводные*
Проверка однородности выбранного параметра
осуществяется с уровнем значимости 2%.

Уровень значимости {self.alpha:.0%}.
Мы хотели бы различать {self.relative_mde:.0%}-ное
изменение целевой метрики
с вероятностью {1 - self.beta:.0%}.
"""

        return problem_text

    def check_homogeneity(self, x, y):
        return ttest_ind(x, y, equal_var=False, alternative=self.get_alternative()).pvalue
