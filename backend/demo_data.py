# Python module for storing our robust deterministic demo data
from models import CodeElement, Fact

DEMO_CODE = """
class DatabaseManager {
    private Table records;

    public void init() {
        records = new Table();
    }

    public void insertRecord(Data d) {
        records.add(d); // writes records
    }

    public Data fetchRecord(int id) {
        return records.get(id); // reads records
    }
}

class UserService {
    private DatabaseManager db;

    public void createUser(User u) {
        Data d = u.toData();
        db.insertRecord(d);
    }

    public User getUser(int id) {
        Data d = db.fetchRecord(id);
        if (d != null) {
            return new User(d);
        }
        return null;
    }
}

class PaymentProcessor {
    private UserService userService;

    public void processPayment(int userId, float amount) {
        User u = userService.getUser(userId);
        if (u.isActive()) {
            // process
        }
    }
}
"""

DEMO_ELEMENTS = [
    CodeElement(id="file_Main", name="Main.java", type="file", filePath="Main.java", startLine=1, endLine=44),
    CodeElement(id="class_DatabaseManager", name="DatabaseManager", type="class", filePath="Main.java", startLine=2, endLine=15),
    CodeElement(id="func_init", name="DatabaseManager.init", type="function", filePath="Main.java", startLine=5, endLine=7),
    CodeElement(id="func_insertRecord", name="DatabaseManager.insertRecord", type="function", filePath="Main.java", startLine=9, endLine=11),
    CodeElement(id="func_fetchRecord", name="DatabaseManager.fetchRecord", type="function", filePath="Main.java", startLine=13, endLine=15),
    CodeElement(id="var_records", name="DatabaseManager.records", type="variable", filePath="Main.java", startLine=3, endLine=3),
    
    CodeElement(id="class_UserService", name="UserService", type="class", filePath="Main.java", startLine=17, endLine=32),
    CodeElement(id="func_createUser", name="UserService.createUser", type="function", filePath="Main.java", startLine=20, endLine=23),
    CodeElement(id="func_getUser", name="UserService.getUser", type="function", filePath="Main.java", startLine=25, endLine=31),
    
    CodeElement(id="class_PaymentProcessor", name="PaymentProcessor", type="class", filePath="Main.java", startLine=34, endLine=43),
    CodeElement(id="func_processPayment", name="PaymentProcessor.processPayment", type="function", filePath="Main.java", startLine=37, endLine=42)
]

DEMO_FACTS = [
    # Containment
    Fact(relation="contains", source="class_DatabaseManager", target="func_init"),
    Fact(relation="contains", source="class_DatabaseManager", target="func_insertRecord"),
    Fact(relation="contains", source="class_DatabaseManager", target="func_fetchRecord"),
    Fact(relation="contains", source="class_DatabaseManager", target="var_records"),
    
    Fact(relation="contains", source="class_UserService", target="func_createUser"),
    Fact(relation="contains", source="class_UserService", target="func_getUser"),
    
    Fact(relation="contains", source="class_PaymentProcessor", target="func_processPayment"),
    
    # Calls
    Fact(relation="calls", source="func_createUser", target="func_insertRecord"),
    Fact(relation="calls", source="func_getUser", target="func_fetchRecord"),
    Fact(relation="calls", source="func_processPayment", target="func_getUser"),
    
    # Data dependencies (Reads/Writes)
    Fact(relation="writes", source="func_insertRecord", target="var_records"),
    Fact(relation="reads", source="func_fetchRecord", target="var_records"),
    Fact(relation="reads", source="func_processPayment", target="class_PaymentProcessor")
]
