# Business Requirements Checker (Backend)

## Описание

Backend-сервис для проверки соответствия документа бизнес-требований заданному шаблону с помощью LLM DeepSeek через API. Принимает два файла (шаблон и требования), отправляет их на анализ в LLM и возвращает структурированный JSON с найденными несоответствиями и резюме.

---

## Требования к окружению

- Python 3.9+
- pip
- Интернет-доступ (для обращения к DeepSeek API)

---

## Установка зависимостей

```bash
cd backend
pip install -r requirements.txt
```

---

## Настройка ключей и промпта

1. **API-ключ DeepSeek**
   - Получите токен на платформе chutes.ai или у вашего администратора.
   - Поместите токен в файл:
     ```
     backend/app/core/deepseek_api_key.txt
     ```
     (только сам токен, без кавычек и пробелов)

2. **Промпт для LLM**
   - Текст промпта хранится в файле:
     ```
     backend/app/core/deepseek_prompt.txt
     ```
   - По умолчанию промпт требует от модели возвращать только JSON без пояснений.
   - Вы можете скорректировать промпт под свои задачи, но обязательно оставьте плейсхолдеры `{template}` и `{requirements}`.

3. **Конфигурация API**
   - Все пути и параметры можно изменить в файле `backend/app/core/config.py`.
   - По умолчанию используется:
     - URL: `https://llm.chutes.ai/v1/chat/completions`
     - Модель: `deepseek-ai/DeepSeek-R1`

---

## Запуск API

```bash
uvicorn app.main:app --reload
```

- По умолчанию сервер будет доступен на `http://127.0.0.1:8000`
- Для проверки работоспособности откройте: `http://127.0.0.1:8000/health`

---

## Запуск frontend (клиентская часть)

1. Перейдите в папку frontend:
   ```bash
   cd ../frontend
   ```
2. Установите зависимости:
   ```bash
   npm install
   ```
3. Запустите dev-сервер:
   ```bash
   npm run dev
   ```
   - По умолчанию приложение будет доступно по адресу: http://localhost:5173

4. Откройте страницу в браузере и загрузите два файла (шаблон и требования), затем нажмите "Analyze Documents".

### Важно
- Frontend по умолчанию ожидает, что backend запущен на http://localhost:8000.
- Если backend работает на другом порту или домене, измените `API_BASE_URL` в файле `frontend/src/utils/api.ts`:
  ```js
  const API_BASE_URL = 'http://localhost:8000/api';
  ```
- Для production-сборки используйте:
  ```bash
  npm run build
  npm run preview
  ```
  (по умолчанию preview будет доступен на http://localhost:4173)

---

## Использование API

### Эндпоинт для анализа требований

```
POST /api/process
```

**Параметры запроса (multipart/form-data):**
- `template` — файл шаблона (PDF, DOCX или TXT)
- `requirements` — файл требований (PDF, DOCX или TXT)

**Пример запроса через curl:**
```bash
curl -X POST http://127.0.0.1:8000/api/process \
  -F "template=@/path/to/template.docx" \
  -F "requirements=@/path/to/requirements.docx"
```

### Пример ответа
```json
{
  "errors": [
    {
      "category": "Structure",
      "location": "1.1",
      "message": "Отсутствует раздел 'Цель документа'",
      "suggestion": "Добавить описание цели создания документа и целевой аудитории",
      "justification": "Шаблон требует явного указания цели документа во введении"
    }
    // ...
  ],
  "summary": "Документ не соответствует шаблону: отсутствуют ключевые разделы, требования не структурированы и не детализированы."
}
```

---

## Обработка ошибок

- Если модель возвращает невалидный JSON, сервис попытается извлечь JSON-блок из текста.
- Если элемент в errors — не словарь, он будет возвращён как текстовое сообщение.
- В случае критических ошибок возвращается HTTP 502 или 500 с описанием причины.

---

## Рекомендации по промпту
- Всегда требуйте от LLM возвращать только JSON без пояснений и markdown.
- Если модель всё равно добавляет лишний текст, используйте регулярные выражения для извлечения JSON.
- Для сложных шаблонов и требований увеличьте max_tokens в конфиге.

---

## Структура проекта (backend)

- `app/main.py` — точка входа FastAPI
- `app/api/routes.py` — описание эндпоинтов
- `app/services/llm_analyzer.py` — логика обращения к DeepSeek
- `app/services/document_processor.py` — обработка файлов
- `app/core/config.py` — конфигурация
- `app/core/deepseek_api_key.txt` — API-ключ
- `app/core/deepseek_prompt.txt` — промпт для LLM

