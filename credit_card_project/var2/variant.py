from decimal import Decimal
from scipy.stats import ttest_ind
from tools import ProblemVariant, VariantTransformer


credit_card_project_variant2 = ProblemVariant(code="credit_card_project_var2")


class TransformerCreditCardProjectVariant2(VariantTransformer):
    def __init__(self, code):
        self.code = code
        self.alpha = Decimal("0.05")
        self.beta = Decimal("0.1")
        self.relative_mde = Decimal("0.08")

    def get_alternative(self):
        return "less"

    def get_metric(self):
        return "PV услуги"

    def get_description(self, random_state):
        problem_text = f"""
*Контекст*
Мы провели конкурентный анализ
и поняли,
что тариф нашей услуги достаточно низкий.
Мы хотим попробовать повысить тариф,
и надеемся,
что снижение конверсии в подключение услуги
компенсируется ростом дохода с этой услуги.
        
*Тест*
Мы проводим тест,
в рамках которого мы разбиваем весь поток
на две части рановероятно,
где одной части (контролю) 
мы будем предлагать старый тариф услуги,
а второй части (тесту) 
- новый тариф услуги.
Целью этого теста
является увеличение доходности услуги.

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
