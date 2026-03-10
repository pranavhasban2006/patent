from engine.fact_extractor import extract_facts_from_code

snippet = """
  saveToDB( Alice );
  saveToDB("Bob");
  saveToDB("Charlie");

  generateReport();
  return 0;
}
"""

elements, facts = extract_facts_from_code(snippet)

print("Elements:")
for e in elements:
    print(f"  {e.type}: {e.name} ({e.id})")

print("\nFacts:")
for f in facts:
    print(f"  {f.source} -> {f.relation} -> {f.target}")

assert any(e.name == "generateReport" for e in elements), "Did not find generateReport"
assert any(e.name == "saveToDB" for e in elements), "Did not find saveToDB"
print("TEST PASSED")
