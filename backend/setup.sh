#!/bin/bash

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 не установлен. Пожалуйста, установите Python 3."
    exit 1
fi

# Удаляем старое виртуальное окружение, если оно существует
if [ -d "venv" ]; then
    echo "Удаление старого виртуального окружения..."
    rm -rf venv
fi

# Создаем новое виртуальное окружение
echo "Создание нового виртуального окружения..."
python3 -m venv venv

# Активируем виртуальное окружение
echo "Активация виртуального окружения..."
source venv/bin/activate

# Обновляем pip и устанавливаем wheel
echo "Обновление pip и установка wheel..."
pip install --upgrade pip
pip install wheel

# Устанавливаем зависимости по одной
echo "Установка зависимостей..."
pip install fastapi
pip install "uvicorn[standard]"
pip install python-multipart
pip install pydantic
pip install pydantic-settings
pip install onnxruntime
pip install transformers
pip install torch
pip install pdfminer.six
pip install python-docx
pip install python-magic
pip install aiofiles
pip install python-jose
pip install passlib
pip install bcrypt

# Создаем необходимые директории
echo "Создание директорий..."
mkdir -p uploads
mkdir -p models

# Добавляем текущую директорию в PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

echo "Установка завершена!"
echo "Для активации виртуального окружения выполните: source venv/bin/activate"

source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"