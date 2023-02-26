# Решение

## ЦПТ, оцениваемая дисперсия

Пусть $l_i$ - расстояние для $i$-й стрелы.
Тогда
```math
l_i^2 = X_i^2 + Y_i^2,
```
где $X_i, Y_i \sim \mathcal{N}(0, a \sigma^2)$.
Тогда $\mathbb{E} l_i^2 = 2 a \sigma^2$
и в силу ЦПТ
```math
\sqrt{n} \frac{\overline{l^2} - 2 a \sigma^2}{S_{l^2}}
\to \mathcal{N}(0, 1).
```
Отсюда доверительный интервал
```math
I = \left(\sqrt{\frac{\overline{l^2}
- z_{1 - \alpha/2} S_{l^2} / \sqrt{n}}{2 a}}, 
\sqrt{\frac{\overline{l^2}
- z_{\alpha/2} S_{l^2} / \sqrt{n}}{2 a}}\right).
```

## Точный доверительный интервал

Заметим, что
```math
l_i^2 = X_i^2 + Y_i^2 = a \sigma^2 Z_i,
```
где $Z_i \sim \chi_2^2$.
Отсюда
```math
\sum_{i=1}^n \frac{l_i^2}{a \sigma^2} 
\sim \chi_{2 n}^2
```
и доверительный интервал
```math
I = \left(\sqrt{\sum_{i=1}^n
\frac{l_i^2}{a z_{1-\alpha/2}}}, 
\sqrt{\sum_{i=1}^n
\frac{l_i^2}{a z_{\alpha/2}}}\right),
```
где $z_{\beta}$ - $\beta$-квантиль
$\chi_{2 n}^2$ распределения.