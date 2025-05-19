from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

app = FastAPI()

@app.get("/")
def index():
    return {"status": "Servidor MCP SSE funcionando"}

@app.api_route("/sse", methods=["GET", "POST"])
async def mcp_sse(request: Request):
    if request.method == "POST":
        body = await request.json()
        text_input = body.get("input", {}).get("text", "")
    else:
        text_input = "sin texto (GET)"

    async def event_generator():
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
