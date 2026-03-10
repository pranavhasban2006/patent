from main import analyze_impact
from models import AnalysisRequest

req = AnalysisRequest(
    sourceCode='''int main() {
  saveToDB("Alice");
  saveToDB("Bob");
  saveToDB("Charlie");

  generateReport();
  return 0;
}''',
    changedElementId="generateReport",
    analysisScope="full"
)

res = analyze_impact(req)
print(res)
