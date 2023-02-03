# Условие

Школа `N` имеет сильный состав
для соревнования в прыжках в длину.
В ней есть несколько сильных спортсменов,
но на соревнования нужно отправить одного.
Тренер Максим вычитал из книги, 
что длина прыжка имеет нормальное распределение с дисперсией $100$,
поэтому тренер решил выбрать лучшего школьника
на основании оценки матожидания длины прыжка.
Помогите Максиму составить симметричный
доверительный интервал этой величины
для каждого студента.

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

Максимальный балл: $4$.
* $+1$ балл, если на выборках размера $1000$ MSE оценки < $0.01$.
* $+1$ балл, если на выборках размера $1000$ MSE оценки < $0.005$.
* $+1$ балл, если на выборках размера $100$ MSE оценки < $0.015$.
* $+1$ балл, если на выборках размера $10$ MSE оценки < $0.09$.

Все вычисления приведены в [Google Colab](https://colab.research.google.com/drive/1jwlp4jgRxRAMGGFJtLyjkVazJnBKXmqC?usp=sharing).
