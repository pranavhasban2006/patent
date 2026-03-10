from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CodeElement(BaseModel):
    id: str  # e.g., "func_authenticate" or "class_User"
    name: str # e.g., "authenticate"
    type: str  # "function", "class", "file", "variable"
    filePath: str
    startLine: int
    endLine: int

class Fact(BaseModel):
    relation: str # "calls", "reads", "writes", "contains"
    source: str   # CodeElement ID
    target: str   # CodeElement ID

class AnalysisRequest(BaseModel):
    sourceCode: str # Plain string if paste, or some file identifier
    changedElementId: str # ID or name of the code element that was changed
    analysisScope: str = "full" # "call", "data", "control", "full"

class ImpactNode(BaseModel):
    id: str
    label: str
    type: str # Element type

class ImpactEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str # e.g., "Data Dependency (reads)"
    animated: bool = False

class ExplanationStep(BaseModel):
    elementId: str
    reasoning: str # e.g., "Impacted because it calls authenticate() which was changed."

class Reasoning(BaseModel):
    controlFlow: List[str]
    dataFlow: List[str]

class AnalysisResponse(BaseModel):
    changedElement: Optional[str] = None
    impactedFunctions: Optional[List[Dict[str, str]]] = None # List of {id, name}
    impactedVariables: Optional[List[Dict[str, str]]] = None # List of {id, name}
    reasoning: Optional[Reasoning] = None
    error: Optional[str] = None
