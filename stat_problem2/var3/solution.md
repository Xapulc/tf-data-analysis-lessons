# Решение

Пусть $X_i \sim R[a, b]$,
где $a$ - известно,
а $b$ - неизвестно.

## ЦПТ, оцениваемая дисперсия

Отметим, что $\mathbb{E} (2 X_i - a) = b$.
Положим $Y_i := 2 X_i - a$.
В силу ЦПТ
```math
\sqrt{n} \frac{\overline{Y} - b}{S_Y}
\to \mathcal{N}(0, 1).
```
Отсюда доверительный интервал
```math
I = \left(\overline{Y} 
- z_{1 - \alpha/2} \frac{S_Y}{\sqrt{n}},
\overline{Y} 
- z_{\alpha/2} \frac{S_Y}{\sqrt{n}}\right).
```

## Точный доверительный интервал

Положим
```math
T(x) := \max\{x_1, \ldots, x_n\} - a.
```
Тогда при $c \in [0, b - a]$
```math
\mathbb{P}_b\left(T(X) \leq c\right)
= \prod_{i=1}^n 
\mathbb{P}_b\left(X_i - a \leq c\right)
= \left(\frac{c}{b - a}\right)^n
= \frac{c^n}{(b - a)^n}.
```
Пусть $\beta \in [0, 1]$,
тогда из соотношения
```math
\beta
= \mathbb{P}_b\left(T(X) \leq z_{\beta}\right)
= \frac{z_{\beta}^n}{(b - a)^n}
```
следует, что
```math
z_{\beta} = (b - a) \sqrt[n]{\beta}.
```
Таким образом, имеем
```math
1 - \alpha
= \mathbb{P}\left((b - a) \sqrt[n]{\alpha / 2}
\leq T(X)
\leq (b - a) \sqrt[n]{1 - \alpha / 2}\right)
= \mathbb{P}\left(a 
+ \frac{T(X)}{\sqrt[n]{1 - \alpha / 2}}
\leq b
\leq a 
+ \frac{T(X)}{\sqrt[n]{\alpha / 2}}\right).
```
Тогда доверительный интервал
```math
I = \left(a + \frac{T(X)}{\sqrt[n]{1 - \alpha / 2}}, 
a + \frac{T(X)}{\sqrt[n]{\alpha / 2}}\right).
```
