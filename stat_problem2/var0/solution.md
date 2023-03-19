# Решение

Пусть $p$ - уровень доверия, $\alpha := 1 - p$.

## ЦПТ, оцениваемая дисперсия

В силу ЦПТ
```math
\sqrt{n} \frac{\overline{X} - a}{S_X} 
\to \mathcal{N}(0, 1).
```
Пусть $z_{\gamma}$ - $\gamma$-квантиль 
стандартного нормального распределения.
Отсюда
```math
1 - \alpha 
\approx \mathsf{P}\left(z_{\alpha / 2} 
\leq \sqrt{n} \frac{\overline{X} - a}{S_X} 
\leq z_{1 - \alpha / 2}\right)
= \mathsf{P}\left(\overline{X}
- z_{1 - \alpha / 2} \frac{S_X}{\sqrt{n}}
\leq a
\leq \overline{X}
- z_{\alpha / 2} \frac{S_X}{\sqrt{n}}\right).
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

В силу свойств нормального распределения
```math
\sqrt{n} \frac{\overline{X} - a}{10} 
\sim \mathcal{N}(0, 1).
```
Пусть $z_{\gamma}$ - $\gamma$-квантиль 
стандартного нормального распределения.
Отсюда
```math
1 - \alpha 
= \mathsf{P}\left(z_{\alpha / 2} 
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
