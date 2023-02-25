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
\sqrt{n} \frac{\overline{X} - a t^2 / 2 + 1/2}{S_X} 
\to \mathcal{N}(0, 1).
```
Пусть $z_{\gamma}$ - $\gamma$-квантиль 
стандартного нормального распределения.
Отсюда
```math
1 - \alpha 
\approx \mathsf{P}\left(z_{\alpha / 2} 
\leq \sqrt{n} \frac{\overline{X} - a t^2 / 2 + 1/2}{S_X} 
\leq z_{1 - \alpha / 2}\right)
= \mathsf{P}\left(2 \overline{X} / t^2 + 1 / t^2
- z_{1 - \alpha / 2} \frac{2 S_X}{t^2 \sqrt{n}}
\leq a
\leq 2 \overline{X} / t^2 + 1 / t^2
- z_{\alpha / 2} \frac{2 S_X}{t^2 \sqrt{n}}\right).
```
Таким образом,
доверительный интервал
```math
\left(2 \overline{X} / t^2 + 1 / t^2
- z_{1 - \alpha / 2} \frac{2 S_X}{t^2 \sqrt{n}},
2 \overline{X} / t^2 + 1 / t^2
- z_{\alpha / 2} \frac{2 S_X}{t^2 \sqrt{n}}\right).
```

## Точный доверительный интервал

Имеем
```math
x_i = a t^2 / 2 + \varepsilon_i,
\quad a t^2 / 2 + \frac{1}{2} - x_i = \frac{1}{2} - \varepsilon_i \sim \exp(1),
\quad n a t^2 / 2 + \frac{n}{2} - n \overline{X} \sim \Gamma(n, 1).
```
Пусть $\gamma_{\beta,n}$ - $\beta$-квантиль
распределения $\Gamma(n, 1)$.
Отсюда
```math
1 - \alpha 
= \mathsf{P}\left(\gamma_{\alpha / 2,n} 
\leq n a t^2 / 2 + \frac{n}{2} - n \overline{X}
\leq \gamma_{1 - \alpha / 2,n}\right)
= \mathsf{P}\left(2 \frac{n \overline{X} + \gamma_{\alpha / 2,n} - n / 2}{t^2 n}
\leq a
\leq 2 \frac{n \overline{X} + \gamma_{1 - \alpha / 2,n} - n / 2}{t^2 n}\right).
```
Таким образом,
доверительный интервал
```math
\left(2 \frac{n \overline{X} + \gamma_{\alpha / 2,n} - n / 2}{t^2 n},
2 \frac{n \overline{X} + \gamma_{1 - \alpha / 2,n} - n / 2}{t^2 n}\right).
```
