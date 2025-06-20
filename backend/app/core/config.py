from pydantic_settings import BaseSettings
from pathlib import Path
import os
import logging
import sys
from typing import List, Set

class Settings(BaseSettings):
    PROJECT_NAME: str = "Business Requirements Checker"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"  # Разрешаем все источники
    ]
    
    # File settings
    UPLOAD_DIR: Path = Path("uploads")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".docx", ".txt"}
    
    # Model settings
    MODEL_PATH: Path = Path("models/bert-base-uncased")
    MODEL_CACHE_DIR: Path = Path("models/cache")
    MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Analysis settings
    MAX_SEQUENCE_LENGTH: int = 512
    BATCH_SIZE: int = 8
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    
    # Encoding settings
    DEFAULT_ENCODING: str = "utf-8"
    
    # DeepSeek API settings
    DEEPSEEK_API_KEY_PATH: str = "app/core/deepseek_api_key.txt"
    DEEPSEEK_PROMPT_PATH: str = "app/core/deepseek_prompt.txt"
    DEEPSEEK_API_URL: str = "https://llm.chutes.ai/v1/chat/completions"
    DEEPSEEK_MODEL: str = "deepseek-ai/DeepSeek-R1"
    
    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

# Создаем экземпляр настроек
settings = Settings()

# Настраиваем логирование
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding=settings.DEFAULT_ENCODING
)

# Устанавливаем кодировку по умолчанию
sys.stdout.reconfigure(encoding=settings.DEFAULT_ENCODING)
sys.stderr.reconfigure(encoding=settings.DEFAULT_ENCODING) 