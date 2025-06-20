import os
import requests
from pathlib import Path
from tqdm import tqdm

def download_file(url: str, filename: str):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)

def main():
    # Создаем директорию для моделей
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    # URL модели
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    model_path = model_dir / "llama-2-7b-chat.Q4_K_M.gguf"
    
    # Скачиваем модель, если её нет
    if not model_path.exists():
        print(f"Downloading model to {model_path}...")
        download_file(model_url, str(model_path))
        print("Download completed!")
    else:
        print("Model already exists!")

if __name__ == "__main__":
    main() 