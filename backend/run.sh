#!/bin/bash

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 не установлен. Пожалуйста, установите Python 3."
    exit 1
fi

# Создаем виртуальное окружение, если его нет
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "Активация виртуального окружения..."
source venv/bin/activate

# Обновляем pip
echo "Обновление pip..."
pip install --upgrade pip

# Устанавливаем зависимости
echo "Установка зависимостей..."
pip install -r requirements.txt

# Создаем необходимые директории
echo "Создание директорий..."
mkdir -p uploads
mkdir -p models

# Добавляем текущую директорию в PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Запускаем сервер
echo "Запуск сервера..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 