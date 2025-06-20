import sys
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_installation():
    try:
        # Проверяем версию Python
        logger.info(f"Python version: {sys.version}")
        
        # Проверяем CUDA
        logger.info(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            logger.info(f"CUDA device: {torch.cuda.get_device_name(0)}")
        
        # Проверяем загрузку токенизатора
        logger.info("Testing tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
        logger.info("Tokenizer loaded successfully")
        
        # Проверяем загрузку модели
        logger.info("Testing model...")
        model = AutoModelForCausalLM.from_pretrained(
            settings.MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        logger.info("Model loaded successfully")
        
        # Тестовый промпт
        test_prompt = "Hello, how are you?"
        inputs = tokenizer(test_prompt, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=50)
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Test response: {response}")
        
        logger.info("All checks passed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Installation check failed: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    check_installation() 