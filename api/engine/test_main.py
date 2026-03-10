from engine.fact_extractor import extract_facts_from_code

snippet = """int main() {
  saveToDB("Alice");
  saveToDB("Bob");
  saveToDB("Charlie");

  generateReport();
  return 0;
}"""

elements, facts = extract_facts_from_code(snippet)

print("Elements:")
for e in elements:
    print(f"  {e.type}: {e.name} ({e.id})")

print("\nFacts:")
for f in facts:
    print(f"  {f.source} -> {f.relation} -> {f.target}")
