"""
Telegram API Proxy Server
Deploy this on an external host (e.g., Render, Railway, Vercel) to bypass HF Spaces egress restrictions.
"""

import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

TELEGRAM_API_BASE = "https://api.telegram.org"

@app.post("/bot{token}/{method}")
async def proxy_telegram(token: str, method: str, request: Request):
    """
    Forwards requests from HF Space -> Proxy -> Telegram API
    """
    try:
        body = await request.json()
        url = f"{TELEGRAM_API_BASE}/bot{token}/{method}"
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=body)
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
            
    except Exception as e:
        return JSONResponse(content={"ok": False, "description": str(e)}, status_code=500)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Telegram Proxy"}
