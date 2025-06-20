import os
import requests
from pathlib import Path
import logging
from tqdm import tqdm
from ..core.config import settings

logger = logging.getLogger(__name__)

def download_file(url: str, destination: Path) -> None:
    """Download a file with progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=destination.name,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

def download_model() -> None:
    """Download the TinyLlama model if it doesn't exist."""
    model_path = settings.MODEL_PATH
    model_dir = model_path.parent
    
    # Create models directory if it doesn't exist
    model_dir.mkdir(parents=True, exist_ok=True)
    
    if not model_path.exists():
        logger.info("Downloading TinyLlama model...")
        # URL для загрузки модели (замените на реальный URL)
        model_url = "https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0/resolve/main/model.onnx"
        try:
            download_file(model_url, model_path)
            logger.info("Model downloaded successfully")
        except Exception as e:
            logger.error(f"Error downloading model: {str(e)}")
            raise
    else:
        logger.info("Model already exists") 