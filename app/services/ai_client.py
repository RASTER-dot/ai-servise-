import httpx
import json
from app.config import settings

async def get_ai_response(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {settings.ai_api_key}", "Content-Type": "application/json"}
    payload = {"model": settings.ai_model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        try:
            content = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            response = await client.post(settings.ai_api_url, content=content)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            raise Exception(f"AI API Error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Network Error: {str(e)}")
        except (KeyError, IndexError):
            raise Exception("Unexpected response format")
