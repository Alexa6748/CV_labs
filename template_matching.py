# -*- coding: utf-8 -*-
"""template matching

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JVZ1br6RDksi6vFEVG7lejRc9karAaAV
"""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

"""# Template matching"""

def sqdiff(image, template):
    I, T = image.astype('float'),template.astype('float')
    H, W = I.shape[0], I.shape[1]
    h, w = T.shape[0], T.shape[1]
    sqd = np.ones_like(image)*np.inf

    for i in range(W-w):
        for j in range(H-h):
            t = (I[j: j+h, i: i+w] - T).ravel()
            sqd[j, i] = t.dot(t)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(-sqd)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv.rectangle(img,top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(-sqd,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle('sqdiff')

    plt.show()

methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
            'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']

def template_matching(img, template, method_num):
    method = getattr(cv, methods[method_num])
    w, h = template.shape[::-1]

    res = cv.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv.rectangle(img,top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(methods[method_num])

    plt.show()

"""Ручной метод sqdiff:"""

img = cv.imread('2.jpg', cv.IMREAD_GRAYSCALE)
template = cv.imread('template2.jpg', cv.IMREAD_GRAYSCALE)
sqdiff(img, template)

"""Ручной метод sqdiff работает правильно, но очень долго. Теперь сравним разные методы из opencv:"""

img = cv.imread('2.jpg', cv.IMREAD_GRAYSCALE)
template = cv.imread('template2.jpg', cv.IMREAD_GRAYSCALE)
for num in range(6):
  template_matching(img, template, num)

"""TM_CCOEFF и TM_CCOEFF_NORMED дают наилучшие результаты без ложных срабатываний.

Результаты работы на прямых изображениях:
"""

for i in range(1, 11):
  s = str(i)
  img = cv.imread(f'{s}.jpg', cv.IMREAD_GRAYSCALE)
  template = cv.imread(f'template{s}.jpg', cv.IMREAD_GRAYSCALE)
  template_matching(img, template, 1)

"""Эффективность на прямых изображениях: 10 из 10

Результаты на косых изображениях:
"""

for i in range(1, 11):
  s = str(i)
  img = cv.imread(f'{s}.jpg', cv.IMREAD_GRAYSCALE)
  template = cv.imread(f'cropped_img_{s}.jpg', cv.IMREAD_GRAYSCALE)
  template_matching(img, template, 1)

"""Эффективность на косых изображениях: 2 из 10

SIFT
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import drive

# Подключение Google Диска
drive.mount('/content/drive')

# Функция для отображения совпадений
def plot_matches(img1, keypoints1, img2, keypoints2, matches):
    img_matches = cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches, outImg=None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    plt.figure(figsize=(15, 7))
    plt.imshow(img_matches)
    plt.axis('off')
    plt.title('Matches')
    plt.show()

# Папки с изображениями
full_images_path = '/content/drive/MyDrive/dataset/'
cropped_images_path = '/content/drive/MyDrive/dataset/pattern/'

# Обработка 40 изображений
for i in range(1, 41):  # Предполагается, что имена файлов от 1.jpg до 40.jpg
    # Загружаем полное изображение и обрезанное изображение
    img1 = cv2.imread(f'{full_images_path}{i}.jpg')  # Полное изображение
    img2 = cv2.imread(f'{cropped_images_path}cropped_img_{i}.jpg')  # Вырезанное изображение

    # Проверка на успешную загрузку изображений
    if img1 is None:
        print(f'Не удалось загрузить полное изображение {i}.jpg.')
        continue
    if img2 is None:
        print(f'Не удалось загрузить обрезанное изображение cropped_img_{i}.jpg.')
        continue

    # Преобразование в градации серого
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Инициализация SIFT
    sift = cv2.SIFT_create()

    # Извлечение ключевых точек и дескрипторов
    keypoints1, descriptors1 = sift.detectAndCompute(img1_gray, None)
    keypoints2, descriptors2 = sift.detectAndCompute(img2_gray, None)

    # Создание сопоставителя
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # Поиск совпадений между дескрипторами
    matches = bf.match(descriptors1, descriptors2)

    # Сортировка совпадений по расстоянию
    matches = sorted(matches, key=lambda x: x.distance)

    # Вывод количества совпадений
    print(f'Number of matches for {i}: {len(matches)}')

    # Отображение совпадений
    plot_matches(img1, keypoints1, img2, keypoints2, matches)