import numpy as np

from scipy.stats import norm, expon, gamma
from tools import ProblemVariant, VariantTransformer


problem2_variant1 = ProblemVariant(code="stat_task2_var1",
                                   input_data_text="""
                                   Два входных значения.
                                   Первое - уровень доверия, число от $0$ до $1$.
                                   Второе - одномерный массив numpy.ndarray
                                   измерений пути (в метрах) одной модели.
                                   """,
                                   output_data_text="""
                                   Кортеж или список из двух значений,
                                   равных левой и правой границе доверительного интервала.
                                   """)


class TransformerProblem2Variant1(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_t = 2
        max_t = 100
        return min_t + (random_state % (max_t - min_t + 1))

    def get_sample(self, iter_size, sample_size, random_state):
        t = self._get_transformed_random_state(random_state)

        a = expon(0.2).rvs(size=iter_size, random_state=t)
        eps = 0.5 - expon.rvs(size=[sample_size, iter_size], random_state=t)
        return (eps + (t**2) * a / 2).T, a

    def get_description(self, random_state):
        t = self._get_transformed_random_state(random_state)

        problem_text = r"""
        На заводе проводится тестирование модели машины для проверки коэффициента ускорения. 
        В рамках эксперимента выбирается $n$ машин этой модели 
        и измеряется пройденный машиной путь 
        """ + f"через количество секунд, равное {t}." + r"""
        Предполагается, что ошибки измерения пути н.о.р.
        и имеют распределение $1/2 - exp(1)$.
        Постройте симметричный доверительный интервал
        для коэффициента ускорения в предположении,
        что движение равноускоренно.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution_description(self, random_state):
        t = self._get_transformed_random_state(random_state)

        return r"""
        Пусть $p$ - уровень доверия, $\alpha := 1 - p$.
        При равноускоренном движении
        $$
        X(t) = \frac{a t^2}{2}
        = """ + f"{(t**2) / 2} a" + r""".
        $$
        Пусть $X_1, \ldots, X_n$ - измерения пути,
        $\varepsilon_1, \ldots, \varepsilon_n
        \sim 1/2 - exp(1)$ - ошибки измерения.
        Тогда
        $$
        X_i = X(t) + \varepsilon_i
        = """ + f"{(t**2) / 2} a" + r""" + \varepsilon_i.
        $$
        
        \section{Асимптотически доверительный интервал}
        
        Отметим, что
        $$
        \mathbb{E} X_i = """ + f"{(t**2) / 2} a" + r""" + \mathbb{E} \varepsilon_i
        = """ + f"{(t**2) / 2} a" + r""" - 1 / 2.
        $$
        В силу подхода с асимптотическим доверительным интервалом
        \begin{multline}
        p \approx \mathbb{P}\left(z_{\alpha / 2} \leq 
        \sqrt{n} \frac{\overline{X} - \left(""" + f"{(t**2) / 2} a" + r""" - 1 / 2\right)}{S_X} 
        \leq z_{1 - \alpha / 2}\right) = \\
        = \mathbb{P}\left(\overline{X} - \frac{z_{1 - \alpha / 2} S_X}{\sqrt{n}}
        \leq """ + f"{(t**2) / 2} a" + r""" - 1 / 2
        \leq \overline{X} - \frac{z_{\alpha / 2} S_X}{\sqrt{n}}\right) = \\
        = \mathbb{P}\left(\frac{1}{""" + f"{(t**2) / 2}" + r"""} 
        \left(1 / 2 + \overline{X} - \frac{z_{1 - \alpha / 2} S_X}{\sqrt{n}}\right)
        \leq a
        \leq \frac{1}{""" + f"{(t**2) / 2}" + r"""} 
        \left(1 / 2 + \overline{X} - \frac{z_{\alpha / 2} S_X}{\sqrt{n}}\right)\right).
        \end{multline}
        Таким образом,
        асимптотический доверительный интервал
        $$
        I = \left(\frac{1}{""" + f"{(t**2) / 2}" + r"""} 
        \left(1 / 2 + \overline{X} - \frac{z_{1 - \alpha / 2} S_X}{\sqrt{n}}\right),
        \frac{1}{""" + f"{(t**2) / 2}" + r"""} 
        \left(1 / 2 + \overline{X} - \frac{z_{\alpha / 2} S_X}{\sqrt{n}}\right)\right).
        $$
        
        \section{Точный доверительный интервал}
        
        Пусть $\delta_i = 1 / 2 - \varepsilon_i$.
        Тогда $\delta_i \sim \exp(1)$.
        
        \subsection{Оценка на основе максимума}
        
        Отметим, что
        $$
        \max\left\{X_1, \ldots, X_n\right\}
        = """ + f"{(t**2) / 2} a" + r""" + 1 / 2 
        - \min\left\{\delta_1, \ldots, \delta_n\right\},
        $$
        где минимум имеет распределение $\exp(n)$,
        не зависящее от параметра $a$.
        Тогда положим
        $$
        g(a; x) := """ + f"{(t**2) / 2} a" + r""" + 1 / 2 
        - \max\left\{x_1, \ldots, x_n\right\}.
        $$
        Проверим свойства из лекции.
        \begin{itemize}
        \item $g(a; X)$ имеет распределение $\exp(n)$,
        не зависящее от параметра $a$.
        \item Квантиль $z_{\beta}$ распределения $g(a; X)$
        является $\beta$-квантилем распределения $\exp(n)$.
        \item При любом фиксированном $x \in \mathbb{R}^n$
        функция $g(a; x)$ растёт по $a$.
        \end{itemize}
        Пусть $g(a; x) = y$.
        Тогда
        $$
        a = \frac{y + \max\left\{x_1, \ldots, x_n\right\} - 1 / 2}{""" + f"{(t**2) / 2}" + r"""}
        = g^{-1}(y; x).
        $$
        Отсюда доверительный интервал
        $$
        I = \left(\frac{z_{\alpha / 2} + \max\left\{x_1, \ldots, x_n\right\} - 1 / 2}{""" + f"{(t**2) / 2}" + r"""},
        \frac{z_{1 - \alpha / 2} + \max\left\{x_1, \ldots, x_n\right\} - 1 / 2}{""" + f"{(t**2) / 2}" + r"""}\right).
        $$
        На практике такой доверительный интервал оказывается достаточно неточным.
        
        \subsection{Оценка на основе суммы}
        
        Отметим, что
        $$
        X_1 + \ldots + X_n
        = n \left(""" + f"{(t**2) / 2} a" + r""" + 1 / 2\right)
        - \left(\delta_1 + \ldots + \delta_n\right),
        $$
        где последняя сумма имеет распределение $\Gamma(n, 1)$,
        не зависящее от параметра $a$.
        Тогда положим
        $$
        g(a; x) := n \left(""" + f"{(t**2) / 2} a" + r""" + 1 / 2\right)
        - \left(x_1 + \ldots + x_n\right).
        $$
        Проверим свойства из лекции.
        \begin{itemize}
        \item $g(a; X)$ имеет распределение $\Gamma(n, 1)$,
        не зависящее от параметра $a$.
        \item Квантиль $z_{\beta}$ распределения $g(a; X)$
        является $\beta$-квантилем распределения $\Gamma(n, 1)$.
        \item При любом фиксированном $x \in \mathbb{R}^n$
        функция $g(a; x)$ растёт по $a$.
        \end{itemize}
        Пусть $g(a; x) = y$.
        Тогда
        $$
        a = \frac{1}{""" + f"{(t**2) / 2}" + r"""}
        \left(\frac{y + x_1 + \ldots + x_n}{n} - \frac{1}{2}\right)
        = g^{-1}(y; x).
        $$
        Отсюда доверительный интервал
        $$
        I = \left(\frac{1}{""" + f"{(t**2) / 2}" + r"""}
        \left(\frac{z_{\alpha / 2} + x_1 + \ldots + x_n}{n} - \frac{1}{2}\right),
        \frac{1}{""" + f"{(t**2) / 2}" + r"""}
        \left(\frac{z_{1 - \alpha / 2} + x_1 + \ldots + x_n}{n} - \frac{1}{2}\right)\right).
        $$
        Это решение в среднем лучше других 
        и является эталонным для данной задачи.
        """

    def get_exact_solution(self, random_state):
        t = self._get_transformed_random_state(random_state)

        def solution(p, x):
            alpha = 1 - p
            loc = (2 * x.mean() - 1) / (t**2)
            scale = 2 / ((t**2) * len(x))
            return gamma.ppf(alpha / 2, len(x), loc=loc, scale=scale), \
                   gamma.ppf(1 - alpha / 2, len(x), loc=loc, scale=scale)

        return solution

    def get_clt_solution(self, random_state):
        t = self._get_transformed_random_state(random_state)

        def solution(p, x):
            alpha = 1 - p
            loc = (2 * x.mean() + 1) / (t**2)
            scale = 2 * np.sqrt(np.var(x)) / ((t**2) * np.sqrt(len(x)))
            return loc - scale * norm.ppf(1 - alpha / 2), \
                   loc - scale * norm.ppf(alpha / 2)

        return solution
