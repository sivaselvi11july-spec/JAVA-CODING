"""
Exhaustive Curriculum and Detailed Topic Data for Java Coding & Object-Oriented Programming (OOP).
Covers all foundational, intermediate, and advanced Java domains with runnable Java 23 code examples.
"""

TOPICS_DATA = {
    # -------------------------------------------------------------
    # CATEGORY 1: THE FOUR PILLARS OF OOP
    # -------------------------------------------------------------
    "encapsulation": {
        "title": "Encapsulation & Data Hiding",
        "category": "The 4 Pillars of OOP",
        "summary": "Bundling data (variables) and methods together while restricting direct access to fields using access modifiers.",
        "details": """### 🛡️ Encapsulation & Data Hiding in Java

**Encapsulation** is the mechanism of wrapping data (variables) and code acting on the data (methods) together as a single unit. In Java, it is achieved by:
1. Declaring class variables as `private` (Data Hiding).
2. Providing `public` getter and setter methods to access and modify field values with validation.

#### Access Modifiers in Java:
| Modifier | Same Class | Same Package | Subclass (Diff Pkg) | World (Everywhere) |
|---|---|---|---|---|
| `private` | ✅ Yes | ❌ No | ❌ No | ❌ No |
| *(default)* | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| `protected` | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| `public` | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

#### Why use Encapsulation?
- **Control over data**: You can validate data before updating (e.g. balance cannot be negative).
- **Flexibility & Maintainability**: Internal implementation can change without breaking client code.
- **Read-only or Write-only**: By selectively providing only getters or only setters.
- **Modern Java Alternative**: For immutable data carriers, modern Java provides `record` classes!""",
        "code": """public class BankAccount {
    // 1. Private fields (hidden from direct outside access)
    private String accountNumber;
    private double balance;

    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        deposit(initialBalance); // Reuse validation logic
    }

    // 2. Controlled getters
    public String getAccountNumber() {
        return accountNumber;
    }

    public double getBalance() {
        return balance;
    }

    // 3. Controlled setters/mutators with business rules
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited $" + amount + ". New balance: $" + balance);
        } else {
            System.out.println("Invalid deposit amount!");
        }
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            System.out.println("Withdrew $" + amount + ". New balance: $" + balance);
            return true;
        }
        System.out.println("Insufficient funds or invalid amount!");
        return false;
    }

    public static void main(String[] args) {
        BankAccount account = new BankAccount("ACC-1002", 500.0);
        account.deposit(250.0);
        account.withdraw(100.0);
        // account.balance = -9999; // COMPILE ERROR: balance has private access!
        System.out.println("Final Account Balance: $" + account.getBalance());
    }
}"""
    },

    "inheritance": {
        "title": "Inheritance (IS-A Relationship)",
        "category": "The 4 Pillars of OOP",
        "summary": "Mechanism where one class acquires the properties and behaviors of a parent class using 'extends'.",
        "details": """### 🧬 Inheritance in Java

**Inheritance** represents an **IS-A relationship** (e.g., a `Dog` IS-A `Animal`). It facilitates code reusability and method overriding.

#### Key Rules & Syntax in Java:
- `extends` keyword is used for inheritance.
- Java supports **Single Inheritance** for classes (a class can have only one direct superclass) to eliminate the Diamond Problem.
- Java supports **Multilevel** (`A -> B -> C`) and **Hierarchical** (`A -> B, A -> C`) inheritance.
- `super` keyword refers to immediate parent class (fields, methods, constructors).
- `final` classes cannot be extended (e.g., `java.lang.String`).
- Constructors are **not** inherited, but the parent constructor is invoked via `super()`.""",
        "code": """class Vehicle {
    protected String brand;
    protected int speed;

    public Vehicle(String brand, int speed) {
        this.brand = brand;
        this.speed = speed;
    }

    public void start() {
        System.out.println(brand + " vehicle is starting.");
    }

    public void displaySpecs() {
        System.out.println("Brand: " + brand + ", Speed: " + speed + " km/h");
    }
}

// Subclass inheriting Vehicle
class ElectricCar extends Vehicle {
    private int batteryCapacity;

    public ElectricCar(String brand, int speed, int batteryCapacity) {
        super(brand, speed); // Calls parent constructor
        this.batteryCapacity = batteryCapacity;
    }

    public void charge() {
        System.out.println(brand + " is charging battery: " + batteryCapacity + " kWh");
    }

    @Override
    public void start() {
        super.start();
        System.out.println("Electric motor engaged silently!");
    }
}

public class Main {
    public static void main(String[] args) {
        ElectricCar tesla = new ElectricCar("Tesla Model 3", 225, 75);
        tesla.start();
        tesla.charge();
        tesla.displaySpecs();
    }
}"""
    },

    "polymorphism": {
        "title": "Polymorphism (Dynamic Dispatch & Overloading)",
        "category": "The 4 Pillars of OOP",
        "summary": "Ability of an action to take multiple forms. Covers Compile-Time (Overloading) and Runtime (Overriding) Polymorphism.",
        "details": """### 🎭 Polymorphism in Java

Polymorphism allows objects of different types to be treated as instances of their common supertype.

#### 1. Compile-Time Polymorphism (Method Overloading / Static Binding)
- Multiple methods in the **same class** with the **same name** but **different parameter signatures** (type, number, or order of arguments).
- **Rule**: Changing only the return type does **NOT** constitute overloading.

#### 2. Runtime Polymorphism (Method Overriding / Dynamic Method Dispatch)
- Subclass provides a specific implementation of a method already declared in its superclass.
- **Rule**: Method signature must match exactly.
- **Rule**: Subclass method cannot have more restrictive access modifier (e.g. `protected` cannot become `private`).
- **Rule**: Static methods cannot be overridden (they are hidden).""",
        "code": """class MathOperations {
    // Compile-Time Polymorphism (Method Overloading)
    public int add(int a, int b) { return a + b; }
    public double add(double a, double b) { return a + b; }
    public int add(int a, int b, int c) { return a + b + c; }
}

abstract class Shape {
    abstract void draw();
    abstract double area();
}

class Circle extends Shape {
    private double radius;
    public Circle(double radius) { this.radius = radius; }
    @Override void draw() { System.out.println("Drawing Circle with radius " + radius); }
    @Override double area() { return Math.PI * radius * radius; }
}

class Rectangle extends Shape {
    private double w, h;
    public Rectangle(double w, double h) { this.w = w; this.h = h; }
    @Override void draw() { System.out.println("Drawing Rectangle (" + w + "x" + h + ")"); }
    @Override double area() { return w * h; }
}

public class Main {
    public static void main(String[] args) {
        MathOperations math = new MathOperations();
        System.out.println("Overloading add(int, int): " + math.add(5, 10));
        System.out.println("Overloading add(double, double): " + math.add(3.5, 2.5));

        System.out.println("\\n--- Dynamic Method Dispatch ---");
        Shape[] shapes = { new Circle(5.0), new Rectangle(4.0, 6.0) };
        for (Shape s : shapes) {
            s.draw(); // Calls actual object's overridden method
            System.out.printf("Area: %.2f\\n", s.area());
        }
    }
}"""
    },

    "abstraction": {
        "title": "Abstraction (Abstract Classes & Interfaces)",
        "category": "The 4 Pillars of OOP",
        "summary": "Hiding internal implementation details and exposing only essential behavior through contracts.",
        "details": """### 🧩 Abstraction: Abstract Classes vs Interfaces

Abstraction isolates **what** an object does from **how** it does it.

#### Comparison Table:
| Feature | Abstract Class | Interface |
|---|---|---|
| **Multiple Inheritance** | No (single class inheritance) | Yes (`implements A, B, C`) |
| **Instance Fields** | Can have mutable instance state | Only `public static final` constants |
| **Constructors** | Yes (`super()` in subclass) | No constructors |
| **Method Types** | Abstract, concrete, final, static | Abstract, `default`, `static` (Java 8+), `private` (Java 9+) |
| **Philosophy** | **"IS-A"** core identity | **"CAN-DO"** peripheral capability |""",
        "code": """interface PaymentGateway {
    void processPayment(double amount);

    default void printReceipt(double amount) {
        System.out.println("Receipt: Processed payment of $" + amount);
    }

    static boolean isValidCurrency(String currency) {
        return "USD".equals(currency) || "EUR".equals(currency) || "INR".equals(currency);
    }
}

abstract class BasePaymentProcessor implements PaymentGateway {
    protected String merchantId;

    public BasePaymentProcessor(String merchantId) {
        this.merchantId = merchantId;
    }

    public void execute(double amount) {
        System.out.println("Merchant [" + merchantId + "] initiating transaction...");
        processPayment(amount);
        printReceipt(amount);
    }
}

class PayPalProcessor extends BasePaymentProcessor {
    public PayPalProcessor(String merchantId) {
        super(merchantId);
    }

    @Override
    public void processPayment(double amount) {
        System.out.println("Connecting to PayPal API... Paid $" + amount + " successfully!");
    }
}

public class Main {
    public static void main(String[] args) {
        BasePaymentProcessor payment = new PayPalProcessor("MERCHANT-77");
        payment.execute(150.0);
        System.out.println("Is USD valid? " + PaymentGateway.isValidCurrency("USD"));
    }
}"""
    },

    # -------------------------------------------------------------
    # CATEGORY 2: OOP DESIGN PRINCIPLES & RELATIONSHIPS
    # -------------------------------------------------------------
    "solid_principles": {
        "title": "SOLID Design Principles",
        "category": "OOP Design & Architecture",
        "summary": "The 5 core principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.",
        "details": """### 🏛️ The SOLID Principles in Java

1. **S - Single Responsibility Principle (SRP)**: A class should have only one reason to change.
2. **O - Open/Closed Principle (OCP)**: Software entities should be open for extension, but closed for modification.
3. **L - Liskov Substitution Principle (LSP)**: Derived classes must be substitutable for base classes without altering correct behavior.
4. **I - Interface Segregation Principle (ISP)**: Clients should not be forced to depend on interfaces they do not use.
5. **D - Dependency Inversion Principle (DIP)**: Depend on abstractions (interfaces), not on concrete implementations.""",
        "code": """interface NotificationService {
    void sendNotification(String message, String recipient);
}

class EmailNotifier implements NotificationService {
    @Override
    public void sendNotification(String message, String recipient) {
        System.out.println("Email sent to " + recipient + ": " + message);
    }
}

class SMSNotifier implements NotificationService {
    @Override
    public void sendNotification(String message, String recipient) {
        System.out.println("SMS sent to " + recipient + ": " + message);
    }
}

// DIP: OrderService depends on NotificationService interface, not EmailNotifier or SMSNotifier
class OrderService {
    private final NotificationService notifier;

    public OrderService(NotificationService notifier) {
        this.notifier = notifier;
    }

    public void completeOrder(String orderId, String customer) {
        System.out.println("Order " + orderId + " completed.");
        notifier.sendNotification("Your order " + orderId + " has shipped!", customer);
    }
}

public class Main {
    public static void main(String[] args) {
        NotificationService email = new EmailNotifier();
        OrderService order1 = new OrderService(email);
        order1.completeOrder("ORD-101", "alice@example.com");

        NotificationService sms = new SMSNotifier();
        OrderService order2 = new OrderService(sms);
        order2.completeOrder("ORD-102", "+1-555-0199");
    }
}"""
    },

    "composition_vs_inheritance": {
        "title": "Composition vs Inheritance (HAS-A vs IS-A)",
        "category": "OOP Design & Architecture",
        "summary": "'Favor object composition over class inheritance' - GoF. Dynamic, loosely coupled design.",
        "details": """### 🧩 Composition vs Inheritance

- **Inheritance (IS-A)**: Tight compile-time coupling. Subclass depends on parent class internal details. Fragile base class problem.
- **Composition (HAS-A)**: Loose coupling. A class contains references to other classes as fields and delegates responsibility. Can swap behaviors dynamically at runtime.""",
        "code": """interface Engine {
    void start();
}

class CombustionEngine implements Engine {
    @Override public void start() { System.out.println("Combustion engine firing pistons! ⛽"); }
}

class ElectricMotor implements Engine {
    @Override public void start() { System.out.println("Electric motor spinning silently! ⚡"); }
}

class Automobile {
    private Engine engine; // HAS-A relationship

    public Automobile(Engine engine) {
        this.engine = engine;
    }

    public void swapEngine(Engine newEngine) {
        this.engine = newEngine;
    }

    public void drive() {
        engine.start();
        System.out.println("Automobile moving forward.");
    }
}

public class Main {
    public static void main(String[] args) {
        Automobile auto = new Automobile(new CombustionEngine());
        auto.drive();

        System.out.println("\\n--- Swapping engine dynamically ---");
        auto.swapEngine(new ElectricMotor());
        auto.drive();
    }
}"""
    },

    # -------------------------------------------------------------
    # CATEGORY 3: DESIGN PATTERNS (CREATIONAL, STRUCTURAL, BEHAVIORAL)
    # -------------------------------------------------------------
    "singleton_pattern": {
        "title": "Singleton Pattern (Thread-Safe)",
        "category": "Design Patterns",
        "summary": "Ensures a class has only one instance and provides a global point of access (Bill Pugh Holder & Enum).",
        "details": """### 🔒 Singleton Pattern in Java

#### 1. Bill Pugh Static Inner Holder (Lazy & Thread-safe without locks):
```java
public class BillPughSingleton {
    private BillPughSingleton() {}
    private static class Holder {
        private static final BillPughSingleton INSTANCE = new BillPughSingleton();
    }
    public static BillPughSingleton getInstance() {
        return Holder.INSTANCE;
    }
}
```

#### 2. Enum Singleton (Recommended by Joshua Bloch - immune to reflection & serialization attacks!):
```java
public enum EnumSingleton {
    INSTANCE;
    public void doSomething() {}
}
```""",
        "code": """public class DatabaseManager {
    private DatabaseManager() {
        System.out.println("DatabaseManager instance created.");
    }

    // Bill Pugh Static Inner Holder: thread-safe, lazy-loaded
    private static class InstanceHolder {
        private static final DatabaseManager INSTANCE = new DatabaseManager();
    }

    public static DatabaseManager getInstance() {
        return InstanceHolder.INSTANCE;
    }

    public void executeQuery(String query) {
        System.out.println("Executing SQL: " + query);
    }

    public static void main(String[] args) {
        DatabaseManager db1 = DatabaseManager.getInstance();
        DatabaseManager db2 = DatabaseManager.getInstance();
        db1.executeQuery("SELECT * FROM users");
        System.out.println("Are db1 and db2 the exact same instance? " + (db1 == db2));
    }
}"""
    },

    "builder_pattern": {
        "title": "Builder Pattern",
        "category": "Design Patterns",
        "summary": "Constructs complex objects step-by-step; eliminates telescoping constructors and enforces immutability.",
        "details": """### 🏗️ Builder Pattern

Eliminates telescoping constructors (e.g. `User(name, email, age, address, phone, zip, country...)`) and provides a readable, fluent API.""",
        "code": """public class Computer {
    private final String cpu;
    private final int ramGB;
    private final boolean hasGpu;
    private final boolean hasBluetooth;

    private Computer(Builder b) {
        this.cpu = b.cpu;
        this.ramGB = b.ramGB;
        this.hasGpu = b.hasGpu;
        this.hasBluetooth = b.hasBluetooth;
    }

    @Override
    public String toString() {
        return "Computer [CPU=" + cpu + ", RAM=" + ramGB + "GB, GPU=" + hasGpu + ", BT=" + hasBluetooth + "]";
    }

    public static class Builder {
        private final String cpu;
        private final int ramGB;
        private boolean hasGpu = false;
        private boolean hasBluetooth = false;

        public Builder(String cpu, int ramGB) {
            this.cpu = cpu;
            this.ramGB = ramGB;
        }

        public Builder setGpu(boolean hasGpu) {
            this.hasGpu = hasGpu;
            return this;
        }

        public Builder setBluetooth(boolean hasBluetooth) {
            this.hasBluetooth = hasBluetooth;
            return this;
        }

        public Computer build() {
            return new Computer(this);
        }
    }

    public static void main(String[] args) {
        Computer gamingPC = new Computer.Builder("Intel i9", 32)
                .setGpu(true)
                .setBluetooth(true)
                .build();
        System.out.println(gamingPC);
    }
}"""
    },

    "factory_pattern": {
        "title": "Factory & Factory Method Pattern",
        "category": "Design Patterns",
        "summary": "Creates objects without exposing the instantiation logic to the client.",
        "details": """### 🏭 Factory Pattern

Defines an interface or method for creating an object, but lets subclasses or a factory class decide which class to instantiate.""",
        "code": """interface Document {
    void open();
}

class PdfDocument implements Document {
    @Override public void open() { System.out.println("Opening PDF Document."); }
}

class WordDocument implements Document {
    @Override public void open() { System.out.println("Opening Word Document."); }
}

class DocumentFactory {
    public static Document createDocument(String type) {
        if ("pdf".equalsIgnoreCase(type)) return new PdfDocument();
        if ("word".equalsIgnoreCase(type)) return new WordDocument();
        throw new IllegalArgumentException("Unknown document type: " + type);
    }
}

public class Main {
    public static void main(String[] args) {
        Document doc1 = DocumentFactory.createDocument("pdf");
        Document doc2 = DocumentFactory.createDocument("word");
        doc1.open();
        doc2.open();
    }
}"""
    },

    "strategy_pattern": {
        "title": "Strategy Pattern",
        "category": "Design Patterns",
        "summary": "Defines a family of interchangeable algorithms and selects them dynamically at runtime.",
        "details": """### 🎯 Strategy Pattern

Encapsulates interchangeable algorithms behind a common interface, allowing client classes to switch strategies without modifying existing code (OCP).""",
        "code": """interface PaymentStrategy {
    void pay(double amount);
}

class CreditCardStrategy implements PaymentStrategy {
    private String cardNumber;
    public CreditCardStrategy(String cardNumber) { this.cardNumber = cardNumber; }
    @Override public void pay(double amount) { System.out.println("Paid $" + amount + " via Card " + cardNumber); }
}

class CryptoStrategy implements PaymentStrategy {
    private String walletAddress;
    public CryptoStrategy(String walletAddress) { this.walletAddress = walletAddress; }
    @Override public void pay(double amount) { System.out.println("Paid $" + amount + " in BTC from " + walletAddress); }
}

class ShoppingCart {
    private PaymentStrategy strategy;
    public void setPaymentStrategy(PaymentStrategy strategy) { this.strategy = strategy; }
    public void checkout(double total) {
        strategy.pay(total);
    }
}

public class Main {
    public static void main(String[] args) {
        ShoppingCart cart = new ShoppingCart();
        cart.setPaymentStrategy(new CreditCardStrategy("****-4432"));
        cart.checkout(99.50);

        cart.setPaymentStrategy(new CryptoStrategy("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"));
        cart.checkout(250.00);
    }
}"""
    },

    "observer_pattern": {
        "title": "Observer Pattern",
        "category": "Design Patterns",
        "summary": "Defines a one-to-many dependency where state changes notify all observers automatically.",
        "details": """### 👁️ Observer Pattern

Used extensively in event handling, pub/sub architectures, and reactive systems.""",
        "code": """import java.util.ArrayList;
import java.util.List;

interface Subscriber {
    void update(String news);
}

class NewsAgency {
    private String latestNews;
    private List<Subscriber> subscribers = new ArrayList<>();

    public void subscribe(Subscriber s) { subscribers.add(s); }
    public void unsubscribe(Subscriber s) { subscribers.remove(s); }

    public void broadcast(String news) {
        this.latestNews = news;
        for (Subscriber s : subscribers) {
            s.update(news);
        }
    }
}

class NewsChannel implements Subscriber {
    private String name;
    public NewsChannel(String name) { this.name = name; }
    @Override public void update(String news) {
        System.out.println("[" + name + "] Breaking News: " + news);
    }
}

public class Main {
    public static void main(String[] args) {
        NewsAgency agency = new NewsAgency();
        NewsChannel bbc = new NewsChannel("BBC");
        NewsChannel cnn = new NewsChannel("CNN");

        agency.subscribe(bbc);
        agency.subscribe(cnn);
        agency.broadcast("Java 23 has officially been released!");
    }
}"""
    },

    # -------------------------------------------------------------
    # CATEGORY 4: JAVA MEMORY, JVM & THE OBJECT CONTRACT
    # -------------------------------------------------------------
    "memory_gc": {
        "title": "JVM Memory & Garbage Collection",
        "category": "Java Memory & Internals",
        "summary": "Stack vs Heap, Metaspace, GC generational architecture, GC roots, and memory leak prevention.",
        "details": """### 🧠 JVM Memory Architecture & Garbage Collection

- **Stack**: Stores method frames, primitives, and object references. Thread-private. Fast automatic cleanup.
- **Heap**: Stores all object instances and arrays. Shared across threads. Managed by Garbage Collection.
- **Metaspace**: Stores class metadata, bytecode, static variables, and runtime constant pool.
- **Garbage Collection (GC)**: Collects unreferenced objects. Uses Young Gen (Eden, S0, S1) and Old/Tenured Gen.""",
        "code": """public class MemoryDemo {
    public static void main(String[] args) {
        // Primitives allocated on Thread Stack
        int localVal = 100;
        
        // Reference 'obj' on Stack; Object instance on Heap
        String obj = new String("Java Heap Object");
        
        System.out.println("Value: " + localVal + ", Ref: " + obj);
        
        // Dereference
        obj = null; // Object is now eligible for Garbage Collection
        
        // Request GC run (JVM may or may not execute immediately)
        System.gc();
        System.out.println("Requested Garbage Collection.");
    }
}"""
    },

    "equals_hashcode": {
        "title": "The equals() and hashCode() Contract",
        "category": "Java Memory & Internals",
        "summary": "The fundamental object contract: why overriding equals requires overriding hashCode for Hash collections.",
        "details": """### 🤝 The `equals()` & `hashCode()` Contract

1. If `a.equals(b)` is `true`, then `a.hashCode() == b.hashCode()` **MUST** be true.
2. If two objects have different hash codes, they cannot be equal.
3. If you forget `hashCode()`, hash collections (`HashMap`, `HashSet`) will look in the wrong hash bucket and fail to find logically equal objects!""",
        "code": """import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

class Student {
    private int id;
    private String name;

    public Student(int id, String name) {
        this.id = id;
        this.name = name;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Student student = (Student) o;
        return id == student.id && Objects.equals(name, student.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name);
    }

    @Override
    public String toString() {
        return "Student(" + id + ", " + name + ")";
    }
}

public class Main {
    public static void main(String[] args) {
        Student s1 = new Student(101, "Alice");
        Student s2 = new Student(101, "Alice");

        Set<Student> set = new HashSet<>();
        set.add(s1);
        set.add(s2); // Will be deduplicated because equals and hashCode match!

        System.out.println("Set size (should be 1): " + set.size());
        System.out.println("Contains s2? " + set.contains(s2));
    }
}"""
    },

    "strings_pool": {
        "title": "String Immutability & String Pool",
        "category": "Java Memory & Internals",
        "summary": "Why Strings are immutable in Java, String Constant Pool (SCP), intern(), and StringBuilder vs StringBuffer.",
        "details": """### 🧵 Strings in Java: Immutability & String Pool

- **Why is String immutable?**
  1. **Security**: Strings carry sensitive database credentials, network URLs, and file paths.
  2. **Thread Safety**: Immutable objects are inherently thread-safe without locks.
  3. **Caching / SCP**: String literals are cached in the String Constant Pool to save memory.
  4. **HashCode caching**: Hash code is calculated once and cached for fast hash lookups.
- **`String` vs `StringBuilder` vs `StringBuffer`**:
  - `String`: Immutable. Creates new objects on every modification.
  - `StringBuilder`: Mutable, not thread-safe (fastest for single-threaded string concatenation).
  - `StringBuffer`: Mutable, thread-safe (all methods are `synchronized`, slower).""",
        "code": """public class StringPoolDemo {
    public static void main(String[] args) {
        // String Literals -> Reused from String Constant Pool (SCP)
        String s1 = "Hello";
        String s2 = "Hello";
        
        // new String -> Explicitly creates new object on the Heap
        String s3 = new String("Hello");

        System.out.println("s1 == s2 (SCP reference check): " + (s1 == s2));       // true
        System.out.println("s1 == s3 (Heap reference check): " + (s1 == s3));       // false
        System.out.println("s1.equals(s3) (Content check): " + s1.equals(s3));     // true
        
        // intern() returns canonical representation from pool
        String s4 = s3.intern();
        System.out.println("s1 == s4 (interned): " + (s1 == s4));                   // true

        // Fast mutable string builder
        StringBuilder sb = new StringBuilder("Java");
        sb.append(" ").append(23);
        System.out.println("StringBuilder result: " + sb.toString());
    }
}"""
    },

    # -------------------------------------------------------------
    # CATEGORY 5: JAVA COLLECTIONS & GENERICS
    # -------------------------------------------------------------
    "collections_framework": {
        "title": "Java Collections Framework",
        "category": "Collections & Generics",
        "summary": "List, Set, Map, and Queue hierarchies: ArrayList vs LinkedList, HashSet vs TreeSet, HashMap internals.",
        "details": """### 📦 Java Collections Framework Architecture

```
                   Iterable
                      |
                  Collection
         /            |             \\
       List          Set           Queue
      /    \\        /   \\             |
ArrayList LinkedList HashSet TreeSet ArrayDeque
                                         |
                                    PriorityQueue

         Map (Separate Hierarchy)
        /   \\
  HashMap  TreeMap
```

#### Key Complexities:
- `ArrayList`: Dynamic array. Fast random access `O(1)`, slow insertion/deletion in middle `O(n)`.
- `LinkedList`: Doubly linked list. Fast insert/delete at ends `O(1)`, slow random access `O(n)`.
- `HashMap`: Hash table with buckets. `O(1)` average lookup. Converts buckets to Red-Black Tree (TreeBin) when bucket length exceeds threshold of 8!
- `TreeSet` / `TreeMap`: Red-Black tree. `O(log n)` sorted traversal.""",
        "code": """import java.util.*;

public class CollectionsDemo {
    public static void main(String[] args) {
        // 1. List: Ordered with duplicates
        List<String> list = new ArrayList<>();
        list.add("Java");
        list.add("Python");
        list.add("Java");
        System.out.println("List: " + list);

        // 2. Set: Unique elements
        Set<String> set = new HashSet<>(list);
        System.out.println("Set (duplicates removed): " + set);

        // 3. Map: Key-Value pairs
        Map<String, Integer> wordCounts = new HashMap<>();
        for (String item : list) {
            wordCounts.put(item, wordCounts.getOrDefault(item, 0) + 1);
        }
        System.out.println("Word Counts Map: " + wordCounts);

        // 4. PriorityQueue: Min-Heap
        Queue<Integer> pq = new PriorityQueue<>();
        pq.offer(40);
        pq.offer(10);
        pq.offer(30);
        System.out.println("PQ poll min: " + pq.poll()); // 10
    }
}"""
    },

    "comparable_vs_comparator": {
        "title": "Comparable vs Comparator",
        "category": "Collections & Generics",
        "summary": "Natural ordering (Comparable: compareTo) vs Custom/Multiple ordering strategies (Comparator: compare).",
        "details": """### ⚖️ Comparable vs Comparator in Java

| Feature | `Comparable<T>` | `Comparator<T>` |
|---|---|---|
| **Package** | `java.lang` | `java.util` |
| **Method** | `int compareTo(T o)` | `int compare(T o1, T o2)` |
| **Modification** | Must modify the original class | Does not modify original class |
| **Ordering** | Single "natural" sorting order | Multiple custom sorting strategies |
| **Usage** | `Collections.sort(list)` | `Collections.sort(list, comparator)` or Lambdas |""",
        "code": """import java.util.*;

class Employee implements Comparable<Employee> {
    private int id;
    private String name;
    private double salary;

    public Employee(int id, String name, double salary) {
        this.id = id;
        this.name = name;
        this.salary = salary;
    }

    public double getSalary() { return salary; }
    public String getName() { return name; }

    // Natural ordering: by ID
    @Override
    public int compareTo(Employee o) {
        return Integer.compare(this.id, o.id);
    }

    @Override
    public String toString() {
        return name + "(ID:" + id + ", $" + salary + ")";
    }
}

public class Main {
    public static void main(String[] args) {
        List<Employee> list = new ArrayList<>(List.of(
            new Employee(103, "Bob", 65000),
            new Employee(101, "Alice", 85000),
            new Employee(102, "Charlie", 72000)
        ));

        // 1. Natural Sort via Comparable (by ID)
        Collections.sort(list);
        System.out.println("Sorted by ID (Comparable): " + list);

        // 2. Custom Sort via Comparator Lambda (by Salary descending)
        list.sort(Comparator.comparingDouble(Employee::getSalary).reversed());
        System.out.println("Sorted by Salary Desc (Comparator): " + list);
    }
}"""
    },

    "generics_wildcards": {
        "title": "Generics & PECS Wildcards",
        "category": "Collections & Generics",
        "summary": "Type parameters, bounded types, type erasure, and PECS (Producer Extends, Consumer Super).",
        "details": """### 🧬 Generics & The PECS Rule

- **Type Erasure**: The JVM erases generic type parameters at compile-time for backward compatibility. `List<String>` and `List<Integer>` both become raw `List` in bytecode.
- **PECS Rule (Joshua Bloch)**:
  - **Producer Extends**: If you only read items from a collection, use `? extends T` (Covariance).
  - **Consumer Super**: If you only write items to a collection, use `? super T` (Contravariance).""",
        "code": """import java.util.ArrayList;
import java.util.List;

public class GenericsDemo {
    // Producer Extends: Reads numbers and calculates sum
    public static double sumOfList(List<? extends Number> numbers) {
        double sum = 0.0;
        for (Number n : numbers) {
            sum += n.doubleValue();
        }
        return sum;
    }

    // Consumer Super: Writes integers into a collection
    public static void addIntegers(List<? super Integer> list) {
        list.add(10);
        list.add(20);
        list.add(30);
    }

    public static void main(String[] args) {
        List<Double> doubleList = List.of(1.5, 2.5, 3.5);
        System.out.println("Sum of doubles: " + sumOfList(doubleList));

        List<Number> numList = new ArrayList<>();
        addIntegers(numList);
        System.out.println("Numbers added: " + numList);
    }
}"""
    },

    # -------------------------------------------------------------
    # CATEGORY 6: JAVA 8+ STREAMS & FUNCTIONAL PROGRAMMING
    # -------------------------------------------------------------
    "streams_lambdas": {
        "title": "Stream API & Lambda Expressions",
        "category": "Modern Java (Java 8 to 23)",
        "summary": "Declarative data processing: filter, map, flatMap, reduce, collect, and functional interfaces.",
        "details": """### 🌊 Java Stream API

Streams provide a declarative pipeline to process collections with intermediate and terminal operations:
- **Intermediate Operations** (Lazy): `filter()`, `map()`, `flatMap()`, `sorted()`, `distinct()`, `limit()`.
- **Terminal Operations** (Executes pipeline): `collect()`, `forEach()`, `reduce()`, `count()`, `anyMatch()`.

#### Key Functional Interfaces:
- `Predicate<T>`: `test(T t) -> boolean`
- `Function<T, R>`: `apply(T t) -> R`
- `Consumer<T>`: `accept(T t) -> void`
- `Supplier<T>`: `get() -> T`""",
        "code": """import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class StreamDemo {
    record Product(String name, String category, double price) {}

    public static void main(String[] args) {
        List<Product> products = List.of(
            new Product("Laptop", "Electronics", 1200.0),
            new Product("Smartphone", "Electronics", 800.0),
            new Product("Coffee Mug", "Kitchen", 15.0),
            new Product("Blender", "Kitchen", 60.0),
            new Product("Headphones", "Electronics", 150.0)
        );

        // 1. Filter, Map, and Collect
        List<String> premiumElectronics = products.stream()
                .filter(p -> "Electronics".equals(p.category()))
                .filter(p -> p.price() > 200.0)
                .map(Product::name)
                .collect(Collectors.toList());

        System.out.println("Premium Electronics: " + premiumElectronics);

        // 2. GroupingBy Category
        Map<String, List<Product>> grouped = products.stream()
                .collect(Collectors.groupingBy(Product::category));
        System.out.println("Categories: " + grouped.keySet());

        // 3. Reduce: Calculate total price
        double totalPrice = products.stream()
                .mapToDouble(Product::price)
                .sum();
        System.out.println("Total Inventory Value: $" + totalPrice);
    }
}"""
    },

    "optional_null_safety": {
        "title": "Optional<T> & Null Safety",
        "category": "Modern Java (Java 8 to 23)",
        "summary": "Eliminating NullPointerExceptions safely using Optional: map, flatMap, orElse, orElseGet.",
        "details": """### 🛡️ Null Safety with `Optional<T>`

`Optional<T>` is a container object used to represent the presence or absence of a value, replacing risky `null` returns.""",
        "code": """import java.util.Optional;

public class OptionalDemo {
    public static Optional<String> findUsernameById(int id) {
        if (id == 42) {
            return Optional.of("Arthur Dent");
        }
        return Optional.empty();
    }

    public static void main(String[] args) {
        // Found case
        Optional<String> user1 = findUsernameById(42);
        String name1 = user1.map(String::toUpperCase).orElse("GUEST");
        System.out.println("User 42: " + name1);

        // Missing case
        Optional<String> user2 = findUsernameById(99);
        String name2 = user2.orElse("Anonymous Guest");
        System.out.println("User 99: " + name2);
    }
}"""
    },

    # -------------------------------------------------------------
    # CATEGORY 7: MODERN JAVA (JAVA 16 TO JAVA 23)
    # -------------------------------------------------------------
    "records_sealed_classes": {
        "title": "Records & Sealed Classes (Java 16 - 17)",
        "category": "Modern Java (Java 8 to 23)",
        "summary": "Immutable data records, sealed classes/interfaces with permits, and pattern matching.",
        "details": """### 🚀 Records & Sealed Classes

- **`record` (Java 16+)**: Automatically generates final fields, canonical constructor, getters (`name()`), `equals()`, `hashCode()`, and `toString()`.
- **`sealed` & `permits` (Java 17+)**: Restricts which classes or interfaces may extend or implement the type.""",
        "code": """// 1. Sealed interface with permits
sealed interface PaymentResult permits Success, Failure {}

// 2. Records implementing sealed interface
record Success(String transactionId, double amount) implements PaymentResult {}
record Failure(String errorCode, String reason) implements PaymentResult {}

public class Main {
    // Pattern matching for switch (Java 21+)
    static String handleResult(PaymentResult result) {
        return switch (result) {
            case Success s -> "Payment OK! ID: " + s.transactionId() + " ($" + s.amount() + ")";
            case Failure f -> "Payment Failed [" + f.errorCode() + "]: " + f.reason();
        };
    }

    public static void main(String[] args) {
        PaymentResult res1 = new Success("TXN-9892", 249.99);
        PaymentResult res2 = new Failure("ERR-503", "Gateway Timeout");

        System.out.println(handleResult(res1));
        System.out.println(handleResult(res2));
    }
}"""
    },

    "virtual_threads": {
        "title": "Virtual Threads (Java 21 Project Loom)",
        "category": "Multithreading & Concurrency",
        "summary": "Lightweight user-mode threads enabling massive throughput with millions of concurrent virtual threads.",
        "details": """### 🧵 Virtual Threads in Java 21+

- Traditional platform threads map 1:1 to OS kernel threads, costing ~1MB of stack memory each.
- **Virtual Threads** are lightweight managed threads running on a small carrier thread pool. You can spawn 1,000,000+ virtual threads simultaneously without running out of memory!""",
        "code": """import java.time.Duration;

public class VirtualThreadDemo {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("Spawning 10,000 Virtual Threads...");
        long start = System.currentTimeMillis();

        Thread[] threads = new Thread[10000];
        for (int i = 0; i < threads.length; i++) {
            final int id = i;
            threads[i] = Thread.ofVirtual().start(() -> {
                // Non-blocking sleep on virtual thread!
                try {
                    Thread.sleep(Duration.ofMillis(10));
                } catch (InterruptedException e) {}
            });
        }

        for (Thread t : threads) {
            t.join();
        }

        long duration = System.currentTimeMillis() - start;
        System.out.println("Completed 10,000 Virtual Threads in: " + duration + " ms!");
    }
}"""
    },

    # -------------------------------------------------------------
    # CATEGORY 8: MULTITHREADING & CONCURRENCY
    # -------------------------------------------------------------
    "multithreading_concurrency": {
        "title": "Multithreading & Concurrency Core",
        "category": "Multithreading & Concurrency",
        "summary": "Thread vs Runnable, synchronized blocks, volatile keyword, race conditions, and ExecutorService.",
        "details": """### ⚡ Multithreading in Java

- **Thread Lifecycle**: NEW -> RUNNABLE -> BLOCKED -> WAITING -> TIMED_WAITING -> TERMINATED.
- **Synchronization**: `synchronized` locks the intrinsic monitor lock of an object to prevent race conditions.
- **`volatile`**: Ensures variable visibility across threads and prevents CPU cache instruction reordering.
- **`ExecutorService`**: Thread pool management avoiding manual thread creation overhead.""",
        "code": """import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class ConcurrencyDemo {
    // Thread-safe atomic counter using CAS (Compare-And-Swap)
    private static final AtomicInteger counter = new AtomicInteger(0);

    public static void main(String[] args) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(4);

        for (int i = 0; i < 1000; i++) {
            executor.submit(() -> {
                counter.incrementAndGet();
            });
        }

        executor.shutdown();
        while (!executor.isTerminated()) {
            Thread.sleep(10);
        }

        System.out.println("Final Atomic Counter Value (expected 1000): " + counter.get());
    }
}"""
    },

    # -------------------------------------------------------------
    # CATEGORY 9: EXCEPTION HANDLING & I/O
    # -------------------------------------------------------------
    "exception_handling": {
        "title": "Exception Handling & try-with-resources",
        "category": "Exception Handling & I/O",
        "summary": "Throwable hierarchy: Checked vs Unchecked, multi-catch, custom exceptions, and AutoCloseable.",
        "details": """### ⚠️ Exception Handling Hierarchy

```
               Throwable
               /       \\
          Exception     Error (Hardware / JVM fatal)
           /     \\
     (Checked)   RuntimeException (Unchecked)
    (IOException) (NullPointer, IndexOutOfBounds)
```

- **Checked Exceptions**: Compiler forces `try-catch` or `throws`.
- **Unchecked Exceptions**: Programming bugs inheriting `RuntimeException`.
- **`try-with-resources`**: Automatically invokes `.close()` on any resource implementing `AutoCloseable`.""",
        "code": """import java.io.StringReader;
import java.io.IOException;

// Custom Checked Exception
class InsufficientBalanceException extends Exception {
    public InsufficientBalanceException(String message) {
        super(message);
    }
}

public class ExceptionDemo {
    public static void withdraw(double balance, double amount) throws InsufficientBalanceException {
        if (amount > balance) {
            throw new InsufficientBalanceException("Requested $" + amount + " but balance is $" + balance);
        }
        System.out.println("Withdrawal approved.");
    }

    public static void main(String[] args) {
        // 1. try-with-resources (AutoCloseable)
        try (StringReader reader = new StringReader("Java 23 Exception Demo")) {
            System.out.println("Read character code: " + reader.read());
        } catch (IOException e) {
            System.err.println("I/O Error: " + e.getMessage());
        }

        // 2. Custom Exception handling
        try {
            withdraw(100.0, 500.0);
        } catch (InsufficientBalanceException e) {
            System.out.println("Caught custom exception: " + e.getMessage());
        }
    }
}"""
    }
}

def get_all_topics():
    return TOPICS_DATA

def get_topic_by_key(key):
    return TOPICS_DATA.get(key)
