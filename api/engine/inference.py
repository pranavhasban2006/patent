from typing import List, Set, Dict, Any, Tuple
from models import CodeElement, Fact, AnalysisResponse, ImpactNode, ImpactEdge, ExplanationStep

def run_inference(elements: List[CodeElement], facts: List[Fact], changed_id: str, scope: str) -> AnalysisResponse:
    """
    Datalog-style inference engine.
    Finds transitive impacts starting from `changed_id`.
    """
    element_map = {e.id: e for e in elements}
    
    # Adjacency structures: source -> List[(target, relation)]
    # For impact, we look at who depends on `changed_id`
    # If A calls B, and B changes, A is impacted. (caller impacted by callee)
    # If A reads V, and V changes, A is impacted.
    # If A writes V, and V changes, A is impacted (or V's readers are impacted).
    
    forward_edges = {} # The dependency graph as viewed for impact analysis
    
    for f in facts:
        # If scope is 'call', only look at 'calls' and 'contains'
        if scope == 'call' and f.relation not in ['calls', 'contains']: continue
        if scope == 'data' and f.relation not in ['reads', 'writes', 'contains']: continue
        
        # Who depends on what?
        # A calls B => A depends on B. Impact flows B -> A
        if f.relation == "calls":
            dependent = f.source
            dependency = f.target
            forward_edges.setdefault(dependency, []).append((dependent, "Called by (control)"))
            
        elif f.relation == "reads":
            dependent = f.source 
            dependency = f.target # data variable
            forward_edges.setdefault(dependency, []).append((dependent, "Read by (data)"))
            
        elif f.relation == "writes":
            dependent = f.target # data variable
            dependency = f.source
            forward_edges.setdefault(dependency, []).append((dependent, "Written by (data)"))
            
        elif f.relation == "contains":
            parent = f.source
            child = f.target
            # If child changes, parent changes. 
            forward_edges.setdefault(child, []).append((parent, "Contained by"))
            # If parent changes, child changes.
            forward_edges.setdefault(parent, []).append((child, "Contains"))

    # Transitive closure (BFS/DFS)
    visited = set()
    queue = [changed_id]
    visited.add(changed_id)
    
    impacted_nodes_info = {} # node_id -> explanation
    impacted_nodes_info[changed_id] = "Original changed element."
    
    edges_traversed = [] # (source, target, label)

    while queue:
        curr = queue.pop(0)
        
        for neighbor, relation_label in forward_edges.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                impacted_nodes_info[neighbor] = f"Transitively impacted because it depends on {curr} via '{relation_label}'."
                edges_traversed.append((curr, neighbor, relation_label))
            else:
                # Add edge anyway for graph completeness if it wasn't added
                if (curr, neighbor, relation_label) not in edges_traversed:
                    edges_traversed.append((curr, neighbor, relation_label))

    # Construct Response
    impacted_elements = []
    seen_elements = set()
    for nid in visited:
        if nid in element_map and nid not in seen_elements:
            seen_elements.add(nid)
            impacted_elements.append(element_map[nid])
            
    impacted_functions = [{"id": el.id, "name": el.name} for el in impacted_elements if el.type == "function"]
    impacted_variables = [{"id": el.id, "name": el.name} for el in impacted_elements if el.type == "variable"]

    control_flow_reasons = []
    data_flow_reasons = []

    for nid, reason in impacted_nodes_info.items():
        if nid == changed_id:
            continue
        if "control" in reason.lower():
            control_flow_reasons.append(f"{nid}: {reason}")
        elif "data" in reason.lower():
            data_flow_reasons.append(f"{nid}: {reason}")
        else:
            control_flow_reasons.append(f"{nid}: {reason}")

    return AnalysisResponse(
        changedElement=changed_id,
        impactedFunctions=impacted_functions,
        impactedVariables=impacted_variables,
        reasoning={
            "controlFlow": control_flow_reasons,
            "dataFlow": data_flow_reasons
        }
    )
