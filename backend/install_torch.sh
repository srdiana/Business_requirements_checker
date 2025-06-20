#!/bin/bash

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем PyTorch
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo "PyTorch установлен!" 