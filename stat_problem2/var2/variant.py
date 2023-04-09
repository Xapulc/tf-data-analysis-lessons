import numpy as np

from scipy.stats import norm, expon, chi2
from tools import ProblemVariant, VariantTransformer


problem2_variant2 = ProblemVariant(code="stat_task2_var2",
                                   input_data_text="""
                                   Два входных значения.
                                   Первое - уровень доверия, число от $0$ до $1$.
                                   Второе - одномерный массив numpy.ndarray
                                   расстояний от места попадания стрелы до центра мишени (в сантиметрах).
                                   """,
                                   output_data_text="""
                                   Кортеж или список из двух значений,
                                   равных левой и правой границе доверительного интервала.
                                   """)


class TransformerProblem2Variant2(VariantTransformer):
    def __init__(self, code, input_data_text, output_data_text):
        self.code = code
        self.input_data_text = input_data_text
        self.output_data_text = output_data_text

    def _get_transformed_random_state(self, random_state):
        min_factor = 2
        max_factor = 50
        return min_factor + (random_state % (max_factor - min_factor + 1))

    def get_sample(self, iter_size, sample_size, random_state):
        factor = self._get_transformed_random_state(random_state)

        sigma = expon(0.5).rvs(size=iter_size, random_state=factor)
        x = norm.rvs(size=[sample_size, iter_size], random_state=factor)
        y = norm.rvs(size=[sample_size, iter_size], random_state=factor+1)

        return np.sqrt(factor * (((x * sigma)**2) + ((y * sigma)**2)).T), sigma

    def get_description(self, random_state):
        factor = self._get_transformed_random_state(random_state)

        problem_text = r"""
        Иван является профессионалом в стрельбе из лука.
        Можно предполагать, что в ортонормированной системе координат
        с центром в центре мишени координаты $(X, Y)$
        места попадания стрелы независимы
        и каждая имеет распределение $\mathcal{N}(0, """ + str(factor) + r""" \sigma^2)$.
        Иван выпускает $n$ стрел и считает расстояния до центра мишени.
        Помогите Ивану определить свой профессионализм,
        построив симметричный доверительный интервал для параметра $\sigma$.
        {\it Указание}: если $X \sim \mathcal{N}(0, 1)$,
        то $X^2$ имеет распределение хи-квадрат
        со степенью свободы $1$.
        """

        return {
            "problem": problem_text,
            "input": self.input_data_text,
            "output": self.output_data_text
        }

    def get_solution_description(self, random_state):
        factor = self._get_transformed_random_state(random_state)

        return r"""
        Пусть $p$ - уровень доверия, $\alpha := 1 - p$.
        Расстояние от центра мишени $r$
        связано с координатами $(x, y)$
        формулой
        $$
        r = \sqrt{x^2 + y^2}.
        $$
        Пусть $R_1, \ldots, R_n$ - измерения расстрояния
        от центра мишени,
        $(X_1, Y_1), \ldots, (X_n, Y_n)$ - координаты попаданий.
        Тогда
        $$
        R_i^2 = X_i^2 + Y_i^2.
        $$
        
        \section{Асимптотически доверительный интервал}
        
        Отметим, что
        $$
        \mathbb{E} R_1^2 = \mathbb{E} X_1^2 + \mathbb{E} Y_1^2
        = """ + f"{2 * factor}" + r""" \sigma^2.
        $$
        Пусть $S_{R^2}^2$ - выборочная дисперсия 
        для $R_1^2, \ldots, R_n^2$.
        В силу подхода с асимптотическим доверительным интервалом
        \begin{multline}
        p \approx \mathbb{P}\left(z_{\alpha / 2} \leq 
        \sqrt{n} \frac{\overline{R^2} - """ + f"{2 * factor}" + r""" \sigma^2}{S_{R^2}} 
        \leq z_{1 - \alpha / 2}\right)
        = \mathbb{P}\left(\overline{R^2} - \frac{z_{1 - \alpha / 2} S_{R^2}}{\sqrt{n}}
        \leq """ + f"{2 * factor}" + r""" \sigma^2
        \leq \overline{R^2} - \frac{z_{\alpha / 2} S_{R^2}}{\sqrt{n}}\right) = \\
        = \mathbb{P}\left(\sqrt{\frac{1}{""" + f"{2 * factor}" + r"""} 
        \left(\overline{R^2} - \frac{z_{1 - \alpha / 2} S_{R^2}}{\sqrt{n}}\right)}
        \leq \sigma
        \leq \sqrt{\frac{1}{""" + f"{2 * factor}" + r"""} 
        \left(\overline{R^2} - \frac{z_{\alpha / 2} S_{R^2}}{\sqrt{n}}\right)}\right).
        \end{multline}
        Таким образом,
        асимптотический доверительный интервал
        $$
        I = \left(\sqrt{\frac{1}{""" + f"{2 * factor}" + r"""} 
        \left(\overline{R^2} - \frac{z_{1 - \alpha / 2} S_{R^2}}{\sqrt{n}}\right)},
        \sqrt{\frac{1}{""" + f"{2 * factor}" + r"""} 
        \left(\overline{R^2} - \frac{z_{\alpha / 2} S_{R^2}}{\sqrt{n}}\right)}\right).
        $$
        
        \section{Точный доверительный интервал}
        
        Как было сказано в условии,
        каждая из величин
        $$
        \frac{X_i}{\sigma \sqrt{""" + f"{2 * factor}" + r"""}},
        \quad \frac{Y_i}{\sigma \sqrt{""" + f"{2 * factor}" + r"""}},
        $$
        имеет хи-квадрат распределение
        со степенью свободы $1$.
        Отсюда величина
        $$
        \frac{R_1^2 + \ldots + R_n^2}{\sigma \sqrt{""" + f"{2 * factor}" + r"""}}
        = \frac{X_1^2 + Y_1^2 + \ldots + X_n^2 + Y_n^2}{\sigma \sqrt{""" + f"{2 * factor}" + r"""}}
        $$
        имеет хи-квадрат распределение со степенью свободы $2 n$.
        Положим
        $$
        g(\sigma; r) := - \frac{r_1^2 + \ldots + r_n^2}{\sigma \sqrt{""" + f"{2 * factor}" + r"""}}.
        $$
        Проверим свойства из лекции.
        \begin{itemize}
        \item $g(\sigma; R)$ имеет распределение $\chi^2(2 n)$,
        не зависящее от параметра $\sigma$.
        \item Квантиль $z_{\beta}$ распределения $g(\sigma; R)$
        явялется противоположным числом
        к $(1-\beta)$-квантилю распределения $\chi^2(2 n)$.
        То есть $z_{\beta} = - \varkappa_{1 - \beta}$,
        где $\varkappa_{1 - \beta}$ - $(1 - \beta)$-квантиль
        распределения $\chi^2(2 n)$.
        \item При любом фиксированном $r \in \mathbb{R}^n$
        функция $g(\sigma; r)$ растёт по $\sigma$.
        \end{itemize}
        Пусть $g(\sigma; r) = s$.
        Тогда
        $$
        \sigma = - \frac{r_1^2 + \ldots + r_n^2}{s \sqrt{""" + f"{2 * factor}" + r"""}}
        = g^{-1}(s; r).
        $$
        Отсюда доверительный интервал
        $$
        I = \left(\frac{R_1^2 + \ldots + R_n^2}{\varkappa_{1 - \alpha / 2} \sqrt{""" + f"{2 * factor}" + r"""}},
        \frac{R_1^2 + \ldots + R_n^2}{\varkappa_{\alpha / 2} \sqrt{""" + f"{2 * factor}" + r"""}}\right).
        $$
        """

    def get_exact_solution(self, random_state):
        factor = self._get_transformed_random_state(random_state)

        def solution(p, x):
            alpha = 1 - p
            scale = (x**2).sum() / factor
            return np.sqrt(scale / chi2.ppf(1 - alpha / 2, 2 * len(x))), \
                   np.sqrt(scale / chi2.ppf(alpha / 2, 2 * len(x)))

        return solution

    def get_clt_solution(self, random_state):
        factor = self._get_transformed_random_state(random_state)

        def solution(p, x):
            alpha = 1 - p
            loc = (x**2).mean()
            scale = np.sqrt(np.var(x**2)) / np.sqrt(len(x))
            return np.sqrt(max((loc - scale * norm.ppf(1 - alpha / 2)) / (2 * factor), 0)), \
                   np.sqrt((loc - scale * norm.ppf(alpha / 2)) / (2 * factor))

        return solution
