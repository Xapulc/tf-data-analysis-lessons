# Решение

При равноускоренном движении
```math
v(t) = a t,
```
где $a$ -- ускорение, $t$ -- время, $v(t)$ -- скорость в момент времени $t$.
В нашем случае $t = 10$, $a$ -- оценивается, известны $v_i = v(t) + \varepsilon_i$,
где $\varepsilon_i + d \sim \exp(1)$ -- независимы

Имеем
```math
v_i = 10 a - d + \varepsilon_i + d,
\quad v_i + d - 10 a = \varepsilon_i + d \sim \exp(1),
\quad \overline{v} + d - 10 a = \frac{\sum_{i=1}^n (\varepsilon_i + d)}{n} \to 1.
```
Отсюда получаем
```math
\widehat{a} := \frac{\overline{v} + d - 1}{10} \to a.
```
Эта оценка
1. несмещённая;
2. состоятельная;
3. асимптотически нормальная.
