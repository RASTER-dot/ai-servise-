from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.config import settings
from app.services.ai_client import get_ai_response

app = FastAPI(title=settings.app_name)

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    result: str

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}

@app.post("/api/generate", response_model=PromptResponse)
async def generate_text(request: PromptRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        result = await get_ai_response(request.prompt)
        return PromptResponse(result=result)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
