"""
Comprehensive Quiz Bank for Java Coding and Object-Oriented Programming (OOP).
High-yield, interview-style conceptual & code-output questions covering all Java domains.
"""

QUIZ_QUESTIONS = [
    {
        "id": "oop_poly_1",
        "topic": "Polymorphism & Dynamic Dispatch",
        "difficulty": "Intermediate",
        "question": "What is the output of the following Java code snippet?",
        "code": """class Parent {
    void show() { System.out.print("P "); }
}
class Child extends Parent {
    void show() { System.out.print("C "); }
}
public class Test {
    public static void main(String[] args) {
        Parent obj = new Child();
        obj.show();
    }
}""",
        "options": [
            "P",
            "C",
            "Compilation Error",
            "Runtime Exception"
        ],
        "correct": 1,
        "explanation": "In Java, method calls on object references are resolved at runtime based on the actual object instance type (Dynamic Method Dispatch / Runtime Polymorphism). Since `obj` references an instance of `Child`, `Child.show()` is executed, printing 'C'."
    },
    {
        "id": "oop_poly_2",
        "topic": "Polymorphism & Overriding Rules",
        "difficulty": "Intermediate",
        "question": "Can an overriding method in a subclass declare a broader access modifier than the superclass method?",
        "code": """class Super {
    protected void display() {}
}
class Sub extends Super {
    public void display() {} // Is this valid?
}""",
        "options": [
            "Yes, visibility can be increased (e.g. protected -> public), but never reduced.",
            "No, the visibility must match exactly.",
            "No, visibility can only be narrowed (e.g. public -> protected).",
            "Only if the method is marked static."
        ],
        "correct": 0,
        "explanation": "According to the Liskov Substitution Principle and the Java Language Specification, an overriding method cannot assign weaker access privileges (e.g. protected to private), but it CAN make it more accessible (e.g. protected to public)."
    },
    {
        "id": "oop_encap_1",
        "topic": "Encapsulation",
        "difficulty": "Beginner",
        "question": "Which principle is primary in achieving Encapsulation in Java?",
        "code": "",
        "options": [
            "Making fields public and writing static methods",
            "Declaring instance variables private and providing public getters/setters with validation",
            "Extending multiple classes with interface implementations",
            "Using method overloading for different parameters"
        ],
        "correct": 1,
        "explanation": "Encapsulation bundles data (fields) and code (methods) together and hides the internal state of an object from direct outside modification. In Java, this is done with private fields and controlled public accessors (getters/setters)."
    },
    {
        "id": "oop_abs_inter_1",
        "topic": "Abstraction & Interfaces",
        "difficulty": "Intermediate",
        "question": "Which statement regarding Interfaces vs Abstract Classes in modern Java (Java 8+) is TRUE?",
        "code": "",
        "options": [
            "Interfaces cannot contain any method implementation.",
            "A class can inherit multiple abstract classes, but only implement one interface.",
            "Interfaces can contain default and static methods with implementations, but cannot have mutable instance state.",
            "Abstract classes cannot have constructors."
        ],
        "correct": 2,
        "explanation": "Since Java 8, interfaces can provide default and static methods with concrete bodies. However, interfaces cannot hold instance variables (only public static final constants), whereas abstract classes can have constructors and instance fields."
    },
    {
        "id": "oop_static_1",
        "topic": "Static Keyword & Method Hiding",
        "difficulty": "Intermediate",
        "question": "Can static methods be overridden in Java?",
        "code": """class A {
    static void test() { System.out.println("A"); }
}
class B extends A {
    static void test() { System.out.println("B"); }
}""",
        "options": [
            "Yes, dynamic polymorphism applies to static methods.",
            "No, static methods belong to the class and are hidden (Method Hiding), not overridden.",
            "Yes, but only if annotated with @Override.",
            "No, defining the same static method in a subclass causes a compilation error."
        ],
        "correct": 1,
        "explanation": "Static methods are resolved at compile-time based on the reference type, not at runtime. When a subclass defines a static method with the exact signature as the superclass, it 'hides' the superclass method instead of overriding it. Using `@Override` on it will cause a compile error."
    },
    {
        "id": "oop_inherit_1",
        "topic": "Inheritance",
        "difficulty": "Beginner",
        "question": "Why does Java NOT support multiple inheritance through classes?",
        "code": "",
        "options": [
            "To avoid the Diamond Problem and architectural ambiguity.",
            "Because the JVM cannot load more than one superclass file.",
            "Because Java does not support interfaces.",
            "Java actually does support multiple class inheritance."
        ],
        "correct": 0,
        "explanation": "Java disallows multiple class inheritance (`class C extends A, B`) to prevent ambiguity (the Diamond Problem), where two superclasses define the same method or state and the runtime cannot determine which implementation to inherit."
    },
    {
        "id": "oop_solid_1",
        "topic": "SOLID Principles",
        "difficulty": "Advanced",
        "question": "Which SOLID principle states that 'Subtypes must be substitutable for their base types without altering program correctness'?",
        "code": "",
        "options": [
            "Single Responsibility Principle (SRP)",
            "Open/Closed Principle (OCP)",
            "Liskov Substitution Principle (LSP)",
            "Dependency Inversion Principle (DIP)"
        ],
        "correct": 2,
        "explanation": "The Liskov Substitution Principle (LSP), introduced by Barbara Liskov, asserts that any subclass or derived class must be usable wherever its superclass is expected without breaking invariants or unexpected behavior."
    },
    {
        "id": "oop_solid_2",
        "topic": "SOLID Principles",
        "difficulty": "Advanced",
        "question": "Which technique best exemplifies the Dependency Inversion Principle (DIP) in Java?",
        "code": "",
        "options": [
            "Directly instantiating concrete database drivers inside controller constructors",
            "Injecting an interface abstraction (e.g. `UserRepository`) via constructor injection rather than depending on `MySQLUserRepository`",
            "Declaring all variables static final",
            "Inheriting deeply across 6 levels of class hierarchy"
        ],
        "correct": 1,
        "explanation": "DIP states high-level modules should not depend on low-level modules; both should depend on abstractions. Injecting interface abstractions rather than hardcoding concrete implementations decouples the architecture."
    },
    {
        "id": "oop_equals_hash_1",
        "topic": "Object Contract",
        "difficulty": "Advanced",
        "question": "What happens if you override `equals()` but DO NOT override `hashCode()` when storing objects in a `HashSet` or `HashMap`?",
        "code": "",
        "options": [
            "The compiler produces a compilation error.",
            "Two logically equal objects might have different hash codes, causing `get()` or `contains()` to fail unexpectedly.",
            "Java automatically generates a matching hashCode based on the overridden equals method.",
            "The JVM throws a `RuntimeException` during runtime."
        ],
        "correct": 1,
        "explanation": "The contract between `equals()` and `hashCode()` mandates: if `a.equals(b)` is true, then `a.hashCode() == b.hashCode()` MUST also be true. If you don't override `hashCode()`, default memory-based hash codes are used, causing hash collisions/mismatches in hash-based collections."
    },
    {
        "id": "oop_patterns_1",
        "topic": "Design Patterns",
        "difficulty": "Intermediate",
        "question": "Which design pattern is best suited when an object's creation involves many optional parameters and complex validation?",
        "code": "",
        "options": [
            "Observer Pattern",
            "Builder Pattern",
            "Adapter Pattern",
            "Strategy Pattern"
        ],
        "correct": 1,
        "explanation": "The Builder pattern separates the construction of a complex object from its representation, avoiding telescoping constructors (constructors with 10 parameters) and ensuring immutability."
    },
    {
        "id": "oop_pass_by_val",
        "topic": "Java Memory & Semantics",
        "difficulty": "Intermediate",
        "question": "What is the output of the following Java program?",
        "code": """public class Test {
    static void modify(int x) { x = 50; }
    public static void main(String[] args) {
        int a = 10;
        modify(a);
        System.out.println(a);
    }
}""",
        "options": [
            "50",
            "10",
            "0",
            "Compilation Error"
        ],
        "correct": 1,
        "explanation": "Java is strictly pass-by-value. For primitive types like `int`, a copy of the primitive value (10) is passed into `modify()`. Modifying `x` inside the method modifies only the local frame copy, leaving `a` unaffected in `main()`."
    },
    {
        "id": "oop_string_pool",
        "topic": "Strings & Memory Architecture",
        "difficulty": "Intermediate",
        "question": "What will `System.out.println(s1 == s2)` print?",
        "code": """String s1 = "Java";
String s2 = new String("Java");
System.out.println(s1 == s2);""",
        "options": [
            "true",
            "false",
            "Compilation Error",
            "Throws NullPointerException"
        ],
        "correct": 1,
        "explanation": "`s1` refers to a literal in the String Constant Pool (SCP). `new String('Java')` explicitly creates a separate object instance on the heap. Since `==` tests object reference equality (memory addresses), `s1 == s2` is `false`. (However, `s1.equals(s2)` would be `true`)."
    },
    {
        "id": "oop_hashmap_tree",
        "topic": "Collections Internals",
        "difficulty": "Advanced",
        "question": "In Java 8+, what happens to a HashMap bucket when the number of colliding elements in that bucket exceeds 8 (assuming overall map capacity >= 64)?",
        "options": [
            "The JVM throws a HashOverflowException.",
            "The bucket's linked list transforms into a balanced Red-Black Tree (TreeNode), improving search time from O(n) to O(log n).",
            "The excess elements are silently discarded.",
            "The bucket switches to a doubly linked list."
        ],
        "correct": 1,
        "explanation": "To defend against hash collision attacks and performance degradation, Java 8 treeifies hash bucket linked lists into Red-Black trees when the bucket length reaches TREEIFY_THRESHOLD (8), reducing search complexity from linear O(n) to logarithmic O(log n)."
    },
    {
        "id": "oop_pecs_rule",
        "topic": "Generics & PECS",
        "difficulty": "Advanced",
        "question": "What does the PECS acronym stand for in Java Generics?",
        "options": [
            "Producer Extends, Consumer Super",
            "Parameter Extends, Class Super",
            "Poly-type Enforces Class Strictness",
            "Priority Elements, Cached Sets"
        ],
        "correct": 0,
        "explanation": "PECS stands for 'Producer Extends, Consumer Super'. If a generic collection produces/reads items (read-only), use `? extends T`. If a collection consumes/accepts items (write-only), use `? super T`."
    },
    {
        "id": "oop_modern_virtual",
        "topic": "Modern Java (Java 21+)",
        "difficulty": "Intermediate",
        "question": "What is the primary advantage of Virtual Threads (Project Loom) introduced in Java 21?",
        "options": [
            "They run single-threaded code 10x faster.",
            "They are lightweight user-mode threads with near-zero memory footprint (~few KB vs 1MB OS thread), enabling millions of concurrent threads.",
            "They completely eliminate the need for synchronization.",
            "They run exclusively on the GPU."
        ],
        "correct": 1,
        "explanation": "Virtual Threads are lightweight threads managed directly by the JVM rather than the OS. They decouple Java threads from OS kernel threads, allowing applications to handle millions of concurrent connections with minimal memory and context-switching overhead."
    },
    {
        "id": "oop_sealed_records",
        "topic": "Modern Java (Java 16 - 17)",
        "difficulty": "Intermediate",
        "question": "What is the role of the `sealed` and `permits` keywords in Java 17?",
        "code": """sealed interface Shape permits Circle, Square {}""",
        "options": [
            "They make the interface private to the package.",
            "They restrict class extension/implementation to only the explicitly permitted subclasses/implementors.",
            "They prevent any subclass from creating instances.",
            "They enforce thread synchronization on all methods."
        ],
        "correct": 1,
        "explanation": "`sealed` classes and interfaces allow authors to control and exhaustively enumerate which other classes or records are allowed to extend or implement them, enabling exhaustive pattern matching in modern Java."
    },
    {
        "id": "oop_try_with_resources",
        "topic": "Exception Handling",
        "difficulty": "Intermediate",
        "question": "Which interface must a class implement to be used in a `try-with-resources` statement?",
        "options": [
            "`java.io.Serializable`",
            "`java.lang.AutoCloseable`",
            "`java.lang.Cloneable`",
            "`java.lang.Runnable`"
        ],
        "correct": 1,
        "explanation": "Any class that implements `java.lang.AutoCloseable` (or its sub-interface `java.io.Closeable`) can be managed by `try-with-resources`. The JVM automatically invokes its `close()` method when the block exits."
    },
    {
        "id": "oop_streams_ops",
        "topic": "Stream API",
        "difficulty": "Intermediate",
        "question": "Which of the following is a TERMINAL operation in the Java Stream API?",
        "options": [
            "`filter()`",
            "`map()`",
            "`flatMap()`",
            "`collect()`"
        ],
        "correct": 3,
        "explanation": "`collect()` is a terminal operation that triggers the execution of the stream pipeline and accumulates the results. `filter()`, `map()`, and `flatMap()` are intermediate operations that return another lazy stream."
    }
]

def get_all_quizzes():
    return QUIZ_QUESTIONS

def get_quizzes_by_topic(topic=None):
    if not topic:
        return QUIZ_QUESTIONS
    topic_lower = topic.lower()
    return [q for q in QUIZ_QUESTIONS if topic_lower in q["topic"].lower()]
