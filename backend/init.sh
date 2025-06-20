#!/bin/bash

# Создаем виртуальное окружение
python3 -m venv venv

# Активируем виртуальное окружение
source venv/bin/activate

# Обновляем pip
pip install --upgrade pip

# Устанавливаем зависимости
pip install -r requirements.txt

# Создаем необходимые директории
mkdir -p uploads

echo "Инициализация завершена!" 