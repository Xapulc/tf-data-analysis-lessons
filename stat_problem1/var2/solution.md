# Решение

При равноускоренном движении
```math
x(t) = \frac{a t^2}{2},
```
где $a$ -- ускорение, $t$ -- время, $x(t)$ -- пройденный путь в момент времени $t$.
В нашем случае $a$ -- оценивается, известны $x_i = x(t) + \varepsilon_i$,
где $\varepsilon_i \sim \text{Laplace}$ -- независимы

Имеем
```math
x_i = \frac{a t^2}{2} + \varepsilon_i,
\quad x_i - \frac{a t^2}{2} = \varepsilon_i \sim \exp(1),
\quad \overline{x} - \frac{a t^2}{2} = \frac{\sum_{i=1}^n \varepsilon_i}{n} \to 0.
```
Отсюда получаем
```math
\widehat{a} := \frac{2 \overline{x}}{t^2} \to a.
```
Эта оценка
1. несмещённая;
2. состоятельная;
3. асимптотически нормальная.
