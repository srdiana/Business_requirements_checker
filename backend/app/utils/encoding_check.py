import sys
import locale
import logging

def check_encoding():
    """Проверяет настройки кодировки системы."""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Default encoding: {sys.getdefaultencoding()}")
    logger.info(f"File system encoding: {sys.getfilesystemencoding()}")
    logger.info(f"Locale encoding: {locale.getpreferredencoding()}")
    logger.info(f"stdout encoding: {sys.stdout.encoding}")
    logger.info(f"stderr encoding: {sys.stderr.encoding}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    check_encoding() 