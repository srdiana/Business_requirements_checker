import subprocess
import sys
import os

def install_requirements():
    # Список необходимых пакетов
    packages = [
        'fastapi',
        'uvicorn',
        'python-multipart',
        'onnxruntime',
        'transformers',
        'torch',
        'pdfminer.six',
        'python-docx',
        'pydantic',
        'python-magic',
        'aiofiles',
        'python-jose',
        'passlib',
        'bcrypt'
    ]
    
    # Установка каждого пакета
    for package in packages:
        print(f"Установка {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    # Проверяем, что мы в виртуальном окружении
    if not hasattr(sys, 'real_prefix') and not hasattr(sys, 'base_prefix'):
        print("Пожалуйста, активируйте виртуальное окружение перед запуском скрипта")
        sys.exit(1)
    
    # Устанавливаем зависимости
    install_requirements()
    print("Все зависимости установлены успешно!") 