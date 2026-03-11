from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import traceback

app = FastAPI(title="Semantic Code Change Impact Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    from models import AnalysisRequest, AnalysisResponse, CodeElement, Fact
    from engine.fact_extractor import extract_facts_from_code
    from engine.inference import run_inference
    from demo_data import DEMO_CODE, DEMO_ELEMENTS, DEMO_FACTS

    @app.get("/")
    def read_root():
        return {"status": "ok", "app": "Semantic Impact Analysis Engine"}

    @app.post("/api/analyze")
    def analyze_impact(request: AnalysisRequest):
        try:
            print(f"[LOG] Received analysis request for changedElement: {request.changedElementId}")
            
            if request.sourceCode.strip() == DEMO_CODE.strip():
                elements = DEMO_ELEMENTS
                facts = DEMO_FACTS
            else:
                elements, facts = extract_facts_from_code(request.sourceCode)
                
            if not any(e.id == request.changedElementId or e.name == request.changedElementId for e in elements):
                return {"error": "Changed element not found in source"}

            resolved_id = next(e.id for e in elements if e.id == request.changedElementId or e.name == request.changedElementId)

            response = run_inference(
                elements=elements,
                facts=facts,
                changed_id=resolved_id,
                scope=request.analysisScope
            )
            
            return response

        except Exception as e:
            return {"error": f"Internal Server Error: {str(e)}"}

    @app.get("/api/demo-data")
    def get_demo_data():
        return {
            "code": DEMO_CODE,
            "elements": DEMO_ELEMENTS,
            "facts": DEMO_FACTS
        }

except Exception as e:
    err_traceback = traceback.format_exc()
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(request: Request, path_name: str):
        return {"error": "FAILED_TO_BOOT_PYTHON_BACKEND", "traceback": err_traceback, "path": path_name}
