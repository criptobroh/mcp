from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

app = FastAPI()

@app.get("/")
def index():
    return {"status": "Servidor MCP SSE funcionando"}

@app.post("/sse")
async def mcp_sse(request: Request):
    body = await request.json()
    text_input = body.get("input", {}).get("text", "")

    async def event_generator():
        # Podés reemplazar esto con llamadas reales a OpenAI si querés.
        yield {
            "event": "message",
            "data": json.dumps({"output": {"text": f"Procesando: {text_input}"}})
        }
        await asyncio.sleep(1)
        yield {
            "event": "message",
            "data": json.dumps({"output": {"text": f"Respuesta final: Recibí '{text_input}'"}})
        }

    return EventSourceResponse(event_generator())
