import logging
import httpx
from fastapi import HTTPException
from ..core.config import settings
from ..models.response import AnalysisResponse, Error
from pathlib import Path
import json as _json
import re

logger = logging.getLogger(__name__)

class LLMAnalyzer:
    def __init__(self):
        # Load API key and prompt from files
        api_key_path = Path(settings.DEEPSEEK_API_KEY_PATH)
        prompt_path = Path(settings.DEEPSEEK_PROMPT_PATH)
        try:
            self.api_key = api_key_path.read_text(encoding='utf-8').strip()
            self.prompt = prompt_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to load DeepSeek API key or prompt: {e}")
            raise HTTPException(status_code=500, detail="Failed to load DeepSeek API key or prompt.")
        self.api_url = settings.DEEPSEEK_API_URL

    async def analyze(self, template_text: str, requirements_text: str) -> AnalysisResponse:
        try:
            # Используем безопасную замену плейсхолдеров вместо .format()
            full_prompt = self.prompt.replace("{template}", template_text).replace("{requirements}", requirements_text)
            payload = {
                "model": settings.DEEPSEEK_MODEL,
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "stream": False,
                "max_tokens": 1024,
                "temperature": 0.7
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload, headers=headers, timeout=60)
                response.raise_for_status()
                data = response.json()
            # DeepSeek returns the result in choices[0].message.content as a string (should be JSON)
            content = data["choices"][0]["message"]["content"]
            logger.error(f"DeepSeek raw content: {content}")
            # Попробуем найти JSON-блок в ответе
            json_match = re.search(r'```json\\s*(\{[\s\S]+?\})\\s*```', content)
            if not json_match:
                # Если нет блока с ```json, ищем просто {...}
                json_match = re.search(r'(\{[\s\S]+\})', content)
            if not json_match:
                logger.error(f"Не найден JSON-блок в ответе: {content}")
                raise HTTPException(status_code=502, detail="DeepSeek response does not contain JSON block.")
            json_str = json_match.group(1)
            try:
                parsed = _json.loads(json_str)
            except Exception as e:
                logger.error(f"Failed to parse extracted JSON: {json_str}")
                raise HTTPException(status_code=502, detail="DeepSeek response JSON block is invalid.")
            errors = []
            for err in parsed.get('errors', []):
                if isinstance(err, dict):
                    errors.append(Error(**err))
                else:
                    # Если ошибка не словарь, а строка или что-то ещё, делаем универсальный Error
                    errors.append(Error(
                        category="LLM Output",
                        location="",
                        message=str(err),
                        suggestion="",
                        justification=""
                    ))
            summary = parsed.get('summary', '')
            return AnalysisResponse(errors=errors, summary=summary)
        except httpx.HTTPStatusError as e:
            logger.error(f"DeepSeek API error: {e.response.text}")
            raise HTTPException(status_code=502, detail=f"DeepSeek API error: {e.response.text}")
        except Exception as e:
            logger.error(f"Error during DeepSeek analysis: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to analyze documents: {str(e)}")