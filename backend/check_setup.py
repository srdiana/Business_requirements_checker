import sys
import importlib
import os

def check_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} установлен")
        return True
    except ImportError:
        print(f"✗ {module_name} не установлен")
        return False

def main():
    # Проверяем, что мы в виртуальном окружении
    if not hasattr(sys, 'real_prefix') and not hasattr(sys, 'base_prefix'):
        print("✗ Виртуальное окружение не активировано")
        return False

    # Проверяем структуру проекта
    required_dirs = ['app', 'models', 'uploads']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"✗ Директория {dir_name} не найдена")
            return False
        print(f"✓ Директория {dir_name} существует")

    # Проверяем необходимые модули
    required_modules = [
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
        'aiofiles'
    ]

    all_modules_ok = True
    for module in required_modules:
        if not check_module(module):
            all_modules_ok = False

    if all_modules_ok:
        print("\n✓ Все проверки пройдены успешно!")
        return True
    else:
        print("\n✗ Некоторые проверки не пройдены")
        return False

if __name__ == "__main__":
    main() 