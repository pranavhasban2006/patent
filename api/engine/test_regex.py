import re

line = "int main() {"
func_match = re.search(r'(?:public|private|protected)?\s*(?:static\s+)?(?:[\w<>:]+)\s+(\w+)\s*\(', line)

if func_match:
    print(f"MATCH: {func_match.group(1)}")
else:
    print("NO MATCH")
