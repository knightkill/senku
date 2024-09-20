from fastapi import FastAPI
from pydantic import BaseModel
from src.llm_handler import LLMHandler
from src.mermaid_handler import MermaidHandler
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.mount("/output", StaticFiles(directory="output"), name="output")


class DiagramRequest(BaseModel):
    text: str


class DiagramResponse(BaseModel):
    mermaid_code: str
    image_path: str


llm_handler = LLMHandler()
mermaid_handler = MermaidHandler()


@app.post("/generate_diagram", response_model=DiagramResponse)
async def generate_diagram(request: DiagramRequest):
    mermaid_code = llm_handler.generate_mermaid_code(request.text)
    image_path = mermaid_handler.convert_mermaid_to_image(mermaid_code)
    if image_path:
        return DiagramResponse(mermaid_code=mermaid_code,
                               image_path=f"http://localhost:8123/output/{os.path.basename(os.path.dirname(image_path))}/diagram.png")
    else:
        return {"error": "Failed to generate diagram"}
