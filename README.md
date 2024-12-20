[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1TZgNlrJXEZLWR06tHC73QcgTo3sFB3cR?usp=sharing)
## Теория
### Template matching
Template matching - метод цифровой обработки изображений для поиска небольших частей изображения, соответствующих шаблону.
TM сопоставляет части изображения с шаблоном и ищет наиболее подходящий регион. Он имеет несколько вариаций операций поиска подходящего региона: метод квадрата разности (sqdiff), метод кросс-корреляции (ccorr) и коэффициентный метод кросс-корреляции (ccoeff).
<br>Формула для sqdiff:
 ![image](https://github.com/user-attachments/assets/2064301c-7230-47dc-8e3a-17201709fda4)

Формула для ccorr:
 ![image](https://github.com/user-attachments/assets/36610db5-115a-445c-9e57-6d43199aa530)

Формула для ccoeff:<br>
  ![image](https://github.com/user-attachments/assets/17aa79ce-f2c3-4f8d-add4-aa0fc8651a13) ![image](https://github.com/user-attachments/assets/2899592a-578e-4a53-81c9-f0b56db8bed1)

, где T – шаблон для поиска, I – оригинальное изображение. Каждый из 3 методов имеет нормализованный вариант.
<br>

### SIFT
SIFT (Scale-Invariant Feature Transform) — это алгоритм, используемый в компьютерном зрении для детекции и описания локальных признаков изображений. Он позволяет находить и классифицировать ключевые точки, которые являются устойчивыми к изменениям масштаба, повороту и частично к изменению освещения и вариациям в точности регистрации.
<br>
Основные компоненты SIFT
<ol>•	Инвариантность к масштабу: Алгоритм ищет ключевые точки на разных масштабах с помощью создания гауссовой пирамиды, что позволяет обнаруживать одни и те же особенности в изображениях, снятых под разным углом или при различных условиях.
<br>•	Инвариантность к повороту: Все ключевые точки описываются с учетом их ориентации, что позволяет алгоритму распознать их независимо от угла поворота изображения.
<br>•	Локальные дескрипторы: Для каждой обнаруженной ключевой точки SIFT создает уникальное представление (descriptor), которое используется для сравнения различных ключевых точек в других изображениях.</ol>

## Описание разработанной системы
### Алгоритм SIFT

Алгоритм SIFT состоит из нескольких ключевых шагов:

1. Создание Гауссовой пирамиды:  
   Из первоначального изображения создаются несколько уровней с различными уровнями размытия. Это позволяет находить ключевые точки на различных масштабах. Разработчики OpenCV запрограммировали эту функциональность внутри класса SIFT.
   
2. Вычисление Разностей Гауссов (DoG):
   Для каждого уровня пирамиды рассчитываются разности между соседними уровнями. Это помогает выделять ключевые точки, которые являются локальными экстремумами в пространстве DoG. SIFT автоматически вычисляет разности между соседними уровнями Гауссовой пирамиды, чтобы выявить ключевые точки.

3. Выбор ключевых точек:
   Ключевые точки отбираются как локальные максимумы и минимумы, и их стабильность проверяется с помощью нескольких критериев. Ключевые точки, которые не соответствуют критериям устойчивости, отбрасываются. SIFT включает механизм удаления неустойчивых ключевых точек, которые не отвечают критериям стабильности. Этот процесс также происходит скрытно внутри функции detectAndCompute().

4. Определение ориентации ключевых точек:
   Каждой ключевой точке присваивается одна или несколько ориентаций на основе градиентов в окрестности ключевой точки. Это позволяет иметь инвариантность к повороту. На этапе определения ориентации, SIFT присваивает ключевым точкам одну или несколько ориентаций на основе градиентов в их окружении.

5. Вычисление дескрипторов:
   Для ключевых точек вычисляются дескрипторы, которые представляют собой векторы, описывающие локальные особенности в окрестности ключевой точки. Обычно используется ориентированный градиент, сгруппированный по углам. Дескрипторы вычисляются для ключевых точек в методе detectAndCompute(). Эти дескрипторы используют информацию о градиентах для описания локальных особенностей.

### Архитектура системы SIFT

Архитектуру системы SIFT можно описать следующим образом:

- Входные данные: Изображение, которое требует анализа.
- Гауссовая пирамида: Модуль, создающий многоуровневую (по различным масштабам) версию изображения.
- Модуль DoG: Этап вычисления разностей Гаусса для выделения ключевых признаков.
- Модуль детекции ключевых точек: Определение стабильных ключевых точек на основе экстремумов.
- Модуль орентации: Распределение ориентаций по ключевым точкам.
- Модуль дескрипторов: Генерация дескрипторов для каждой ключевой точки на основе информации о градиентах.
- Выходные данные: Набор ключевых точек и их дескрипторов, готовых для дальнейшей обработки, таких как сопоставление или классификация.

## Результаты
### Результаты работы на прямых изображениях:
#### OpenCV:
![image](https://github.com/user-attachments/assets/029e1f6a-2b98-4035-b6cc-8fb3de090669)
![image](https://github.com/user-attachments/assets/66ec4aa2-3d3f-4520-b80c-932417025170)
![image](https://github.com/user-attachments/assets/899e7120-885b-40ea-b006-8b80e2a7870d)

#### Ручной метод sqdiff:
![image](https://github.com/user-attachments/assets/95a310dc-d81a-4094-986b-6973454e20df)

### Результаты на косых изображениях:
#### Template Matching
![image](https://github.com/user-attachments/assets/323c4386-f544-4106-91f5-d8933a5b2c31)
#### SIFT
![image](https://github.com/user-attachments/assets/540562e0-2ce9-4a9d-b571-4ac7369fcf66)
## Выводы по работе
Для задач, связанных с сопоставлением шаблонов, рекомендуется использовать методы, такие как TM_CCOEFF и TM_CCOEFF_NORMED, в условиях, когда изображения имеют одинаковую ориентацию и масштаб.
В случаях, когда изображения могут быть искажены или наклонены, стоит рассмотреть использование методов, таких как SIFT или другие алгоритмы, основанные на ключевых точках, которые обеспечивают большую устойчивость к изменениям.
## Заключение
В будущем можно исследовать комбинации различных методов для повышения точности сопоставления, а также рассмотреть использование других алгоритмов, таких как ORB или SURF, для сравнения их эффективности с SIFT.
