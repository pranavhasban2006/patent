from engine.fact_extractor import extract_facts_from_code

snippet = """#include <iostream>
#include <string>
#include <vector>

using namespace std;

int userCount = 0;
int adminCount = 0;
vector<string> userDB;
vector<string> adminDB;

void logToConsole(const string& msg) { cout << "[LOG] " << msg << endl; }
void saveUser(const string& user) { userDB.push_back(user); userCount++; logToConsole("User saved: " + user); }
void saveAdmin(const string& admin) { adminDB.push_back(admin); adminCount++; logToConsole("Admin saved: " + admin); }
bool validateName(const string& name) { return name.length() >= 3; }
bool validateUser(const string& user) { return validateName(user); }
bool validateAdmin(const string& admin) { return validateName(admin) && admin != "root"; }
void registerUser(const string& user) { if (validateUser(user)) { saveUser(user); } else { logToConsole("Invalid user rejected: " + user); } }
void registerAdmin(const string& admin) { if (validateAdmin(admin)) { saveAdmin(admin); } else { logToConsole("Invalid admin rejected: " + admin); } }
int calculateTotalAccounts() { return userCount + adminCount; }
double calculateAdminRatio() { if (userCount == 0) return 0.0; return static_cast<double>(adminCount) / userCount; }
void generateUserReport() { cout << "Users (" << userCount << "): "; for (const auto& u : userDB) cout << u << " "; cout << endl; }
void generateAdminReport() { cout << "Admins (" << adminCount << "): "; for (const auto& a : adminDB) cout << a << " "; cout << endl; }
void generateSummaryReport() { int total = calculateTotalAccounts(); double ratio = calculateAdminRatio(); cout << "================ SUMMARY ================" << endl; cout << "Total Accounts: " << total << endl; cout << "Admin/User Ratio: " << ratio << endl; cout << "========================================" << endl; }

void generateFullReport() {
    generateUserReport();
    generateAdminReport();
    generateSummaryReport();
}

int main() {
    registerUser("Alice"); registerUser("Bo"); registerUser("Charlie");
    registerAdmin("Dave"); registerAdmin("root"); registerAdmin("Eve");
    generateFullReport();
    return 0;
}"""

elements, facts = extract_facts_from_code(snippet)
print("Elements:")
for e in elements:
    if "generate" in e.name or e.name == "main":
        print(f"  {e.type}: {e.name} ({e.id})")

print("\nRelevant Facts:")
for f in facts:
    if "generateFullReport" in f.source or "generateFullReport" in f.target:
        print(f"  {f.source} -> {f.relation} -> {f.target}")
