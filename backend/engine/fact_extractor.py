import re
from typing import Tuple, List
from models import CodeElement, Fact
import uuid

def extract_facts_from_code(source_code: str) -> Tuple[List[CodeElement], List[Fact]]:
    """
    Very lightweight heuristic extractor for generic pasted code to support the 
    'paste code into a Monaco editor' feature when not using the demo data.
    """
    elements = []
    facts = []
    
    seen_ids = set()
    def get_unique_id(base_id):
        if base_id not in seen_ids:
            seen_ids.add(base_id)
            return base_id
        idx = 2
        while f"{base_id}_{idx}" in seen_ids:
            idx += 1
        new_id = f"{base_id}_{idx}"
        seen_ids.add(new_id)
        return new_id
        
    lines = source_code.splitlines()
    
    # Basic class detection
    current_class = None
    
    # We will track brackets to map function scopes
    # func_scopes: lists of tuples (startLine, endLine, func_id)
    func_scopes = []
    current_func_id = None
    current_brace_depth = 0
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Detect classes or structs (C++ style)
        class_match = re.search(r'(?:class|struct)\s+(\w+)', line)
        if class_match:
            class_name = class_match.group(1)
            el_id = get_unique_id(f"class_{class_name}")
            elements.append(CodeElement(
                id=el_id, name=class_name, type="class", 
                filePath="input.txt", startLine=line_num, endLine=line_num
            ))
            current_class = el_id
            
        # Detect functions (C/C++/Java basic heuristic)
        # Matches: void funcName() or int funcName (args)
        func_match = re.search(r'(?:public|private|protected)?\s*(?:static\s+)?(?:[\w<>:]+)\s+(\w+)\s*\(', line)
        if func_match and not class_match and "new " not in line and "=" not in line.split("(")[0]:
            func_name = func_match.group(1)
            # We no longer ignore "main"
            if func_name not in ["if", "for", "while", "switch", "catch"]:
                el_id = get_unique_id(f"func_{func_name}")
                elements.append(CodeElement(
                    id=el_id, name=func_name, type="function",
                    filePath="input.txt", startLine=line_num, endLine=line_num
                ))
                if current_class:
                    facts.append(Fact(relation="contains", source=current_class, target=el_id))
                
                # Start tracking this function scope
                current_func_id = el_id
                current_brace_depth = 0
                    
        # Basic variable/global detection
        var_match = re.search(r'(?:extern\s+)?(?:[\w<>:]+)\s+(\w+)(?:\s*=|;)', line)
        if var_match and not func_match and not class_match and "return " not in line:
            var_name = var_match.group(1)
            el_id = get_unique_id(f"var_{var_name}")
            elements.append(CodeElement(
                id=el_id, name=var_name, type="variable",
                filePath="input.txt", startLine=line_num, endLine=line_num
            ))
            if current_class:
                facts.append(Fact(relation="contains", source=current_class, target=el_id))
        
        # Brace tracking to determine function scopes
        if current_func_id:
            current_brace_depth += line.count('{')
            current_brace_depth -= line.count('}')
            
            # If we drop to 0 depth, this function block is strictly over
            # unless the function definition was a single line without braces e.g. void do() ;
            if current_brace_depth <= 0 and line.count('{') > 0:
                 # It closed. 
                 func_el = next(e for e in elements if e.id == current_func_id)
                 func_el.endLine = line_num
                 current_func_id = None
            elif current_brace_depth < 0:
                 # Closed even when we didn't see an open brace on the definition line
                 func_el = next(e for e in elements if e.id == current_func_id)
                 func_el.endLine = line_num
                 current_func_id = None
                 
    # Close any unclosed scopes at the end of the file
    if current_func_id:
        func_el = next(e for e in elements if e.id == current_func_id)
        func_el.endLine = len(lines)

    # Add GLOBAL_SCOPE for lines outside any function
    if "func_GLOBAL_SCOPE" not in seen_ids:
        get_unique_id("func_GLOBAL_SCOPE")
        elements.append(CodeElement(
            id="func_GLOBAL_SCOPE", name="GLOBAL_SCOPE", type="function",
            filePath="input.txt", startLine=1, endLine=len(lines)
        ))

    # Naive call & data detection
    func_names = {e.name: e.id for e in elements if e.type == "function"}
    var_names = {e.name: e.id for e in elements if e.type == "variable"}
    
    for i, line in enumerate(lines):
        line_num = i + 1
        caller_id = None
        
        # Check which function's scope this line belongs to
        for el in elements:
            if el.type == "function" and el.name != "GLOBAL_SCOPE":
                if el.startLine <= line_num <= el.endLine:
                    caller_id = el.id
                    break
                    
        if not caller_id:
            caller_id = "func_GLOBAL_SCOPE"
            
        # Detect implicit function calls
        for match in re.finditer(r'\b([a-zA-Z_]\w*)\s*\(', line):
            called_func = match.group(1)
            # Skip common keywords
            if called_func in ["if", "for", "while", "switch", "catch"]:
                continue
                
            if called_func not in func_names:
                new_id = get_unique_id(f"func_{called_func}")
                func_names[called_func] = new_id
                elements.append(CodeElement(
                    id=new_id, name=called_func, type="function",
                    filePath="input.txt", startLine=i+1, endLine=i+1
                ))
            
            fid = func_names[called_func]
            if caller_id != fid and fid != caller_id: # Avoid self-calling loop for main declaration
                # Remove decl_line check because implicit functions have startLine == line_num
                # and explicit definitions are already ignored by the `if` check on line 147
                facts.append(Fact(relation="calls", source=caller_id, target=fid))
                
        for vname, vid in var_names.items():
            # word match for variable
            if re.search(r'\b' + vname + r'\b', line):
                # if not the declaration line
                var_start = next((e.startLine for e in elements if e.id == vid), -1)
                if i + 1 != var_start:
                    if "=" in line and line.split("=")[0].find(vname) != -1:
                        facts.append(Fact(relation="writes", source=caller_id, target=vid))
                    else:
                        facts.append(Fact(relation="reads", source=caller_id, target=vid))
                
    # Deduplicate facts
    unique_facts = []
    seen_facts = set()
    for f in facts:
        sig = f"{f.relation}_{f.source}_{f.target}"
        if sig not in seen_facts:
            seen_facts.add(sig)
            unique_facts.append(f)
            
    return elements, unique_facts
