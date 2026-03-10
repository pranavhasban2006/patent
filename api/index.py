from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from models import AnalysisRequest, AnalysisResponse, CodeElement, Fact
from engine.fact_extractor import extract_facts_from_code
from engine.inference import run_inference
from demo_data import DEMO_CODE, DEMO_ELEMENTS, DEMO_FACTS

app = FastAPI(title="Semantic Code Change Impact Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "app": "Semantic Impact Analysis Engine"}

@app.post("/api/analyze")
def analyze_impact(request: AnalysisRequest):
    try:
        print(f"[LOG] Received analysis request for changedElement: {request.changedElementId}")
        
        # Depending on input string, either use Demo facts or try a heuristic
        if request.sourceCode.strip() == DEMO_CODE.strip():
            elements = DEMO_ELEMENTS
            facts = DEMO_FACTS
            print(f"[LOG] Using demo facts. Parsed {len([e for e in elements if e.type == 'function'])} functions and {len([e for e in elements if e.type == 'variable'])} variables.")
        else:
            # For non-demo code, use our resilient parser
            elements, facts = extract_facts_from_code(request.sourceCode)
            func_count = sum(1 for e in elements if e.type == "function")
            var_count = sum(1 for e in elements if e.type == "variable")
            print(f"[LOG] Parsed {func_count} functions and {var_count} global variables/structs.")
            
        if not any(e.id == request.changedElementId or e.name == request.changedElementId for e in elements):
            return {"error": "Changed element not found in source"}

        # Resolve exact ID if user provided name
        resolved_id = next(e.id for e in elements if e.id == request.changedElementId or e.name == request.changedElementId)

        print(f"[LOG] Extracted {len(facts)} dependency facts. Running inference...")
        # Run inference engine
        response = run_inference(
            elements=elements,
            facts=facts,
            changed_id=resolved_id,
            scope=request.analysisScope
        )
        
        return response

    except Exception as e:
        print(f"Error during analysis: {e}")
        return {"error": f"Internal Server Error: {str(e)}"}

@app.get("/api/demo-data")
def get_demo_data():
    return {
        "code": DEMO_CODE,
        "elements": DEMO_ELEMENTS,
        "facts": DEMO_FACTS
    }
