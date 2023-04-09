import numpy as np

from decimal import Decimal
from scipy.stats import norm, expon, chi2, uniform
from tools import ProblemVariant, VariantTransformer


problem2_variant3 = ProblemVariant(code="stat_task2_var3",
                                   input_data_text="""
                                   Два входных значения.
                                   Первое - уровень доверия, число от $0$ до $1$.
                                   Второе - одномерный массив numpy.ndarray
                                   уровней значимостей.
                                   """,
                                   output_data_text="""
                                   Кортеж или список из двух значений,
                                   равных левой и правой границе доверительного интервала.
                                   """)


class TransformerProblem2Variant3(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_alpha_numerator = 5
        max_alpha_numerator = 100
        alpha_denominator = 1000

        alpha_numerator = min_alpha_numerator + ((random_state - 44) % (max_alpha_numerator - min_alpha_numerator + 1))
        return Decimal(alpha_numerator) / Decimal(alpha_denominator)

    def get_sample(self, iter_size, sample_size, random_state):
        min_alpha = self._get_transformed_random_state(random_state)
        min_alpha_random_state = int(1000 * min_alpha)
        float_min_alpha = float(min_alpha)

        max_alpha = uniform.rvs(size=iter_size, random_state=max(min_alpha_random_state - 12, 0))
        alpha = uniform.rvs(size=[sample_size, iter_size], random_state=min_alpha_random_state)
        return (float_min_alpha + alpha * (max_alpha - float_min_alpha)).T, max_alpha

    def get_description(self, random_state):
        min_alpha = self._get_transformed_random_state(random_state)

        problem_text = f"""
        Пётр пытается понять алгоритм генерации 
        уровня значимости в ДЗ по проверке гипотез.
        Известно, что генерируемый уровень значимости
        имеет равномерное распределение
        $[{min_alpha}, b]$.
        Помогите Петру определить распределение,
        построив доверительный интервал для $b$.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution_description(self, random_state):
        min_alpha = self._get_transformed_random_state(random_state)

        return r"""
        Пусть $p$ - уровень доверия, $\alpha := 1 - p$.
        Пусть $X_1, \ldots, X_n$ - измерения уровней значимости.
        
        \section{Асимптотически доверительный интервал}
        
        Отметим, что
        $$
        \mathbb{E} X_1 = \frac{""" + f"{min_alpha}" + r""" + b}{2}.
        $$
        В силу подхода с асимптотическим доверительным интервалом
        \begin{multline}
        p \approx \mathbb{P}\left(z_{\alpha / 2} \leq 
        \sqrt{n} \frac{\overline{X} - (""" + f"{min_alpha}" + r""" + b) / 2}{S_X} 
        \leq z_{1 - \alpha / 2}\right) = \\
        = \mathbb{P}\left(\overline{X} - \frac{z_{1 - \alpha / 2} S_X}{\sqrt{n}}
        \leq \frac{""" + f"{min_alpha}" + r""" + b}{2}
        \leq \overline{X} - \frac{z_{\alpha / 2} S_X}{\sqrt{n}}\right) = \\
        = \mathbb{P}\left(2 \overline{X} - """ + f"{min_alpha}" + r""" 
        - \frac{2 z_{1 - \alpha / 2} S_X}{\sqrt{n}}
        \leq b
        \leq 2 \overline{X} - """ + f"{min_alpha}" + r""" 
        - \frac{2 z_{\alpha / 2} S_X}{\sqrt{n}}\right).
        \end{multline}
        Таким образом,
        асимптотический доверительный интервал
        $$
        I = \left(2 \overline{X} - """ + f"{min_alpha}" + r""" 
        - \frac{2 z_{1 - \alpha / 2} S_X}{\sqrt{n}},
        2 \overline{X} - """ + f"{min_alpha}" + r""" 
        - \frac{2 z_{\alpha / 2} S_X}{\sqrt{n}}\right).
        $$
        
        \section{Точный доверительный интервал}
        
        Как было отмечено в бонусе к лекции,
        параметры равномерного распределения
        лучше оценивать с помощью максимума.
        Попробуем использовать это соображение.
        
        Отметим, что
        $$
        X_i - """ + f"{min_alpha}" + r""" 
        \sim R[0, b - """ + f"{min_alpha}" + r"""],
        \quad \frac{X_i - """ + f"{min_alpha}" + r"""}{b - """ + f"{min_alpha}" + r"""}
        \sim R[0, 1].
        $$
        Таким образом, случайная величина
        $$
        \max\left\{\frac{X_1 - """ + f"{min_alpha}" + r"""}{b - """ + f"{min_alpha}" + r"""},
        \ldots, \frac{X_n - """ + f"{min_alpha}" + r"""}{b - """ + f"{min_alpha}" + r"""}\right\}
        $$
        как максимум независимых равномерных $[0, 1]$ величин
        имеет распределение, не зависящее от $b$.
        
        Положим
        $$
        g(b; x) := - \frac{\max\{x_1, \ldots, x_n\} - """ + f"{min_alpha}" + r"""}{b - """ + f"{min_alpha}" + r"""}.
        $$
        Проверим свойства из лекции.
        \begin{itemize}
        \item $g(b; X)$ имеет распределение,
        не зависящее от параметра $b$.
        \item При любом фиксированном $x \in \mathbb{R}^n$
        функция $g(b; x)$ растёт по $b$.
        \end{itemize}
        Найдём $\beta$-квантиль $g(b; X)$.
        Пусть $t \in (-1, 0)$.
        Тогда
        \begin{multline}
        1 - \mathbb{P}\left(g(b; X) \leq t\right)
        = \mathbb{P}\left(g(b; X) > t\right) = \\
        = \mathbb{P}\left(\max\left\{\frac{X_1 - """ + f"{min_alpha}" + r"""}{b - """ + f"{min_alpha}" + r"""},
        \ldots, \frac{X_n - """ + f"{min_alpha}" + r"""}{b - """ + f"{min_alpha}" + r"""}\right\} < -t\right) = \\
        = \prod_{i=1}^n \mathbb{P}\left(\frac{X_1 - """ + f"{min_alpha}" + r"""}{b - """ + f"{min_alpha}" + r"""} < -t\right)
        = (-t)^n.
        \end{multline}
        Отсюда
        $$
        \beta = \mathbb{P}\left(g(b; X) \leq t\right) = 1 - (-t)^n,
        \quad t = - \sqrt[n]{1 - \beta}.
        $$
        Так мы получили $\beta$-квантиль распределения $g(b; X)$.
        
        Найдём обратную функцию.
        Пусть $g(b; x) = y$.
        Тогда
        $$
        b = """ + f"{min_alpha}" + r""" - \frac{\max\{x_1, \ldots, x_n\} - """ + f"{min_alpha}" + r"""}{y}
        = g^{-1}(y; x).
        $$
        Отсюда доверительный интервал
        $$
        I = \left(""" + f"{min_alpha}" + r"""
        + \frac{\max\{X_1, \ldots, X_n\} - """ + f"{min_alpha}" + r"""}{\sqrt[n]{1 - \alpha / 2}},
        """ + f"{min_alpha}" + r"""
        + \frac{\max\{X_1, \ldots, X_n\} - """ + f"{min_alpha}" + r"""}{\sqrt[n]{\alpha / 2}}.
        $$
        """

    def get_exact_solution(self, random_state):
        min_alpha = self._get_transformed_random_state(random_state)
        float_min_alpha = float(min_alpha)

        def solution(p, x):
            alpha = 1 - p
            t = x.max() - float_min_alpha
            n = len(x)
            return float_min_alpha + t / ((1 - alpha / 2)**(1 / n)), \
                   float_min_alpha + t / ((alpha / 2)**(1 / n))

        return solution

    def get_clt_solution(self, random_state):
        min_alpha = self._get_transformed_random_state(random_state)
        float_min_alpha = float(min_alpha)

        def solution(p, x):
            alpha = 1 - p
            y = 2 * x - float_min_alpha
            loc = y.mean()
            scale = np.sqrt(y.var() / len(x))
            return max(loc - scale * norm.ppf(1 - alpha / 2), 0), \
                   loc - scale * norm.ppf(alpha / 2)

        return solution
