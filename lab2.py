import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.interpolate import interp1d

# Ініціалізація списків та змінних
ФК = [1]  # "множник ґрат": ДС антени в площині Н
ФЕ = [1]  # ДС антени в площині Е
Ф1Е = [1]  # ДС напівхвильового вібратора в площині Е

кут_кроки = [0]  # кути θ
ШГП_ФК = 0  # Ширина головної пелюстки в площині ФК
ШГП_ФЕ = 0  # Ширина головної пелюстки в площині ФЕ

Нулі = []  # нульові кути
N = 7  # Кількість елементів
F = 600e6  # Частота в Гц

хвиля = round(299792458 / F, 4)
відстань_елем = round(0.25 * хвиля, 4)
хвильове_число = round((2 * np.pi) / хвиля, 4)

# Розрахунок кутів θ
m_values = np.arange(1, 11)
аргумент = np.clip(1 - (m_values * хвиля) / (N * відстань_елем), -1, 1)
кут_мін = np.arccos(аргумент)
theta_min = np.round(np.degrees(кут_мін[кут_мін <= np.pi / 2]), 2)

# Основний цикл для розрахунку ДС
кут_θ = np.arange(0.01, np.pi / 2, 0.01)  # Створення масиву тета
кут_кроки.extend(np.degrees(кут_θ))  # Додавання кутів у градусах

# Розрахунок значень ДС
множник1 = np.abs(np.cos(np.pi / 2 * np.sin(кут_θ)) / np.cos(кут_θ))
множник2 = np.abs(np.sin((N * хвильове_число * відстань_елем * (1 - np.cos(кут_θ)) / 2)) /
                   (N * np.sin((хвильове_число * відстань_елем * (1 - np.cos(кут_θ))) / 2)))
результат = множник1 * множник2

# Додавання обчислених значень у списки
Ф1Е.extend(множник1)
ФК.extend(множник2)
ФЕ.extend(результат)

# Точний розрахунок ширини головної пелюстки
інтерп_множник2 = interp1d(множник2, кут_θ, kind='linear', bounds_error=False, fill_value='extrapolate')
інтерп_результат = interp1d(результат, кут_θ, kind='linear', bounds_error=False, fill_value='extrapolate')

точний_ШГП_ФК = інтерп_множник2(0.707)
точний_ШГП_ФЕ = інтерп_результат(0.707)

ШГП_ФК = np.round(2 * np.degrees(точний_ШГП_ФК), 2)
ШГП_ФЕ = np.round(2 * np.degrees(точний_ШГП_ФЕ), 2)

Нулі = np.round(np.degrees(кут_θ[множник2 < 0.01]), 2)

# Визначення напрямків максимального випромінювання
піки_ФК, _ = find_peaks(ФК)
кут_макс_ФК = np.degrees(кут_θ[піки_ФК])
пікові_значення_ФК = np.array(ФК)[піки_ФК]

піки_ФЕ, _ = find_peaks(ФЕ)
кут_макс_ФЕ = np.degrees(кут_θ[піки_ФЕ])
пікові_значення_ФЕ = np.array(ФЕ)[піки_ФЕ]

# Розмір графіка
plt.figure(figsize=(12, 8))

# Побудова графіків з новими стилями
plt.plot(кут_кроки, Ф1Е, label="$ F_{1E}(θ) $", linestyle="-.", color="purple", linewidth=3)
plt.plot(кут_кроки, ФК, label="$ F_{C}(θ) = F_{H}(θ) $", linestyle=":", color="darkgreen", linewidth=3)
plt.plot(кут_кроки, ФЕ, label="$ F_{E}(θ) $", linestyle="--", color="orange", linewidth=3)

# Позначення знайдених інтерпольованих точок
plt.plot(ШГП_ФК / 2, 0.707, marker="*", color='yellow', markersize=8, label="ШГП у площині ФК")
plt.plot(ШГП_ФЕ / 2, 0.707, marker="*", color='pink', markersize=8, label="ШГП у площині ФЕ")

# Позначення нулів
plt.plot(Нулі, [0] * len(Нулі), 'ko', markersize=5)

# Позначення максимумів на графіку
plt.plot(кут_макс_ФК, пікові_значення_ФК, "s", color="cyan", markersize=6, label="$ \\theta_{max} $ ФК")
plt.plot(кут_макс_ФЕ, пікові_значення_ФЕ, "s", color="magenta", markersize=6, label="$ \\theta_{max} $ ФЕ")

# Позначення рівня половинної потужності (0.707)
plt.axhline(y=0.707, color="gray", linestyle="-.", label="Половинна потужність (0.707)", linewidth=0.8)

# Форматування графіка
plt.xlabel("θ" + '°', fontsize=14, fontweight='bold')
plt.ylabel("$ F_H(θ), F_E(θ) $", fontsize=14, fontweight='bold')
plt.legend(loc="upper right", fontsize=12)
plt.grid(which='both', linestyle=':', linewidth=0.6, color='black')
plt.title("Діаграма спрямованості директорної антени", fontsize=16, fontweight='bold')

# Задаємо розміри клітинок
plt.xticks(np.arange(0, 100, 5), fontsize=12)
plt.yticks(np.arange(0, 1.2, 0.1), fontsize=12)

# Задаємо ліміти відображення
plt.ylim(-0.01, 1.01)
plt.xlim(0, 90.5)

plt.show()