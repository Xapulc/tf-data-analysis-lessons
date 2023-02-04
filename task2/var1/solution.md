# Условие

На заводе проводится тестирование модели машины для проверки коэффициента ускорения. 
В рамках эксперимента выбирается `n` машин этой модели 
и измеряется пройденный машиной путь через `10` секунд.
Предполагается, что ошибки измерения пути н.о.р.
и имеют распределение $1/2 - exp(1)$.
Постройте симметричный доверительный интервал
для коэффициента ускорения.

# Решение

Пусть $p$ - уровень доверия, $\alpha := 1 - p$.
При равноускоренном движении
```math
x(t) = \frac{a t^2}{2},
```
где $a$ -- ускорение, $t$ -- время, $x(t)$ -- пройденный путь в момент времени $t$.
В нашем случае $t = 10$, $a$ -- оценивается, известны $x_i = x(t) + \varepsilon_i$,
где $\varepsilon_i \sim 1/2 - exp(1)$ -- независимы.

## ЦПТ, оцениваемая дисперсия

В силу ЦПТ
```math
\sqrt{n} \frac{\overline{X} - 50 a + 1/2}{S_X} 
\to \mathcal{N}(0, 1).
```
Пусть $z_{\gamma}$ - $\gamma$-квантиль 
стандартного нормального распределения.
Отсюда
```math
1 - \alpha 
\approx \mathsf{P}\left(z_{\alpha / 2} 
\leq \sqrt{n} \frac{\overline{X} - 50 a + 1/2}{S_X} 
\leq z_{1 - \alpha / 2}\right)
= \mathsf{P}\left(\overline{X} / 50 + 1 / 100
- z_{1 - \alpha / 2} \frac{S_X}{\sqrt{50 n}}
\leq a
\leq \overline{X} / 50 + 1 / 100
- z_{\alpha / 2} \frac{S_X}{\sqrt{50 n}}\right).
```
Таким образом,
доверительный интервал
```math
\left(\overline{X}
- z_{1 - \alpha / 2} \frac{S_X}{\sqrt{n}},
\overline{X}
- z_{\alpha / 2} \frac{S_X}{\sqrt{n}}\right).
```

## ЦПТ, известная дисперсия

В силу ЦПТ
```math
\sqrt{n} \frac{\overline{X} - a}{10} 
\to \mathcal{N}(0, 1).
```
Пусть $z_{\gamma}$ - $\gamma$-квантиль 
стандартного нормального распределения.
Отсюда
```math
1 - \alpha 
\approx \mathsf{P}\left(z_{\alpha / 2} 
\leq \sqrt{n} \frac{\overline{X} - a}{10} 
\leq z_{1 - \alpha / 2}\right)
= \mathsf{P}\left(\overline{X}
- z_{1 - \alpha / 2} \frac{10}{\sqrt{n}}
\leq a
\leq \overline{X}
- z_{\alpha / 2} \frac{10}{\sqrt{n}}\right).
```
Таким образом,
доверительный интервал
```math
\left(\overline{X}
- z_{1 - \alpha / 2} \frac{10}{\sqrt{n}},
\overline{X}
- z_{\alpha / 2} \frac{10}{\sqrt{n}}\right).
```

## Точный доверительный интервал

Имеем
```math
x_i = 50 a + \varepsilon_i,
\quad 50 a + \frac{1}{2} - x_i = \frac{1}{2} - \varepsilon_i \sim \exp(1),
\quad 50 a n + \frac{n}{2} - n \overline{X} \sim \Gamma(n, 1).
```
Пусть $\gamma_{\beta,n}$ - $\beta$-квантиль
распределения $\Gamma(n, 1)$.
Отсюда
```math
1 - \alpha 
= \mathsf{P}\left(\gamma_{\alpha / 2,n} 
\leq 50 a n + \frac{n}{2} - n \overline{X}
\leq \gamma_{1 - \alpha / 2,n}\right)
= \mathsf{P}\left(\frac{n \overline{X} + \gamma_{\alpha / 2,n} - n / 2}{50 n}
\leq a
\leq \frac{n \overline{X} + \gamma_{1 - \alpha / 2,n} - n / 2}{50 n}\right).
```

# Оценка задачи

Максимальный балл: $6$. За каждый выполненный пункт $+1$ балл.

| Размер выборки  | Уровень доверия | Ограничение на частоту непопадания в доверительный интервал | Ограничение на среднюю длину доверительного интервала |
| --------------- | --------------- | ----------------------------------------------------------- | ----------------------------------------------------- |
| $1000$          | $99$%           | $2$%                                                        | $2$                                                   |
| $1000$          | $90$%           | $12$%                                                       | $1.1$                                                 |
| $100$           | $70$%           | $32$%                                                       | $2.2$                                                 |
| $100$           | $90$%           | $11$%                                                       | $3.3$                                                 |
| $10$            | $95$%           | $10$%                                                       | $13$                                                  |
| $10$            | $90$%           | $11$%                                                       | $10.6$                                                |

Все вычисления приведены в [Google Colab](https://colab.research.google.com/drive/1XXHPOFiP4GZRVhckeQrZa67tSt4vqkSA?usp=sharing).
