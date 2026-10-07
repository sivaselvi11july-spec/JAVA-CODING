"""
Comprehensive Knowledge Base and Intent Resolution Engine for Java & OOP.
Maps questions, keywords, concepts, comparisons, and error debugging to authoritative answers and runnable Java code.
"""

import re
from engine.topics_data import TOPICS_DATA

# Comparison Topics & Explanations
COMPARISONS = {
    "abstract_vs_interface": {
        "title": "Abstract Class vs Interface in Java",
        "keywords": ["abstract class vs interface", "interface vs abstract class", "difference between abstract and interface"],
        "content": """### ⚖️ Abstract Class vs Interface in Java

| Criteria | Abstract Class | Interface |
|---|---|---|
| **Multiple Inheritance** | ❌ No (single class inheritance) | ✅ Yes (`implements A, B, C`) |
| **Instance Variables** | Can have instance fields with mutable state | Only `public static final` constants |
| **Constructors** | ✅ Yes (invoked via `super()`) | ❌ No constructors |
| **Method Implementation** | Abstract and concrete instance methods | Abstract, `default`, `static` (Java 8+), `private` (Java 9+) |
| **Access Modifiers** | `private`, `protected`, `public` | Methods are `public` by default |
| **Philosophy** | **"IS-A"** core identity and shared state | **"CAN-DO"** peripheral behavioral contract |

```java
// Interface: Capability Contract
interface Drivable {
    void drive();
    default void honk() { System.out.println("Beep beep!"); }
}

// Abstract Class: Shared Identity & State
abstract class Vehicle {
    protected String brand;
    public Vehicle(String brand) { this.brand = brand; }
    public abstract void fuelType();
}

class SportsCar extends Vehicle implements Drivable {
    public SportsCar(String brand) { super(brand); }
    @Override public void fuelType() { System.out.println(brand + " takes Premium Gasoline."); }
    @Override public void drive() { System.out.println(brand + " accelerating to 200 km/h!"); }
}

public class Main {
    public static void main(String[] args) {
        SportsCar car = new SportsCar("Ferrari");
        car.fuelType();
        car.drive();
        car.honk();
    }
}
```"""
    },

    "overloading_vs_overriding": {
        "title": "Method Overloading vs Method Overriding",
        "keywords": ["overloading vs overriding", "overriding vs overloading", "method overloading and method overriding"],
        "content": """### ⚖️ Method Overloading vs Method Overriding

| Criteria | Method Overloading | Method Overriding |
|---|---|---|
| **Type of Polymorphism** | Compile-Time (Static Binding) | Runtime (Dynamic Binding) |
| **Location** | Within the **same class** | Between **Superclass and Subclass** |
| **Method Name** | Same | Same |
| **Method Signature** | **Must differ** (parameters type, number, or order) | **Must match exactly** |
| **Return Type** | Can be different | Must match (or covariant subtype) |
| **Private/Static/Final** | Can be overloaded | Cannot be overridden |
| **Access Modifier** | Any | Subclass **cannot reduce visibility** (e.g. `protected` cannot become `private`) |

```java
class Calculator {
    // Overloading: Same method name, different parameter lists
    int multiply(int a, int b) { return a * b; }
    double multiply(double a, double b) { return a * b; }
}

class Animal {
    // Superclass method
    void speak() { System.out.println("Animal sound"); }
}

class Dog extends Animal {
    // Overriding: Exact same signature, dynamic runtime dispatch
    @Override
    void speak() { System.out.println("Woof! 🐶"); }
}

public class Main {
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        System.out.println("Overloaded: " + calc.multiply(3, 4));

        Animal a = new Dog(); // Dynamic Binding
        a.speak();            // Calls Dog.speak()
    }
}
```"""
    },

    "string_builder_buffer": {
        "title": "String vs StringBuilder vs StringBuffer",
        "keywords": ["string vs stringbuilder", "stringbuilder vs stringbuffer", "string stringbuilder stringbuffer"],
        "content": """### ⚖️ String vs StringBuilder vs StringBuffer

| Feature | `String` | `StringBuilder` | `StringBuffer` |
|---|---|---|---|
| **Mutability** | **Immutable** (new object on modification) | **Mutable** | **Mutable** |
| **Thread Safety** | ✅ Safe (immutable) | ❌ Not Thread-Safe | ✅ Thread-Safe (`synchronized`) |
| **Performance** | Slow for frequent concatenation | **Fastest** (no synchronization overhead) | Slower than `StringBuilder` |
| **Memory** | Uses String Constant Pool | Heap | Heap |
| **When to use** | Fixed text, hash keys, security | Single-threaded string concatenation | Multi-threaded shared concatenation |

```java
public class Main {
    public static void main(String[] args) {
        // 1. String: creates 3 objects in memory
        String str = "Hello";
        str = str + " " + "World";

        // 2. StringBuilder: modifies internal char/byte buffer in place
        StringBuilder sb = new StringBuilder("Java");
        sb.append(" ").append(23).append(" is Fast!");

        System.out.println(str);
        System.out.println(sb.toString());
    }
}
```"""
    },

    "equals_vs_double_equals": {
        "title": "== vs .equals() in Java",
        "keywords": ["== vs equals", "equals vs ==", "difference between == and equals"],
        "content": """### ⚖️ `==` vs `.equals()` in Java

- **`==` Operator**:
  - Compares **primitives**: checks value equality (e.g., `5 == 5` is `true`).
  - Compares **objects**: checks **reference equality** (memory address identity). Returns `true` only if both variables point to the exact same memory address!
- **`.equals()` Method**:
  - Defined in `java.lang.Object`.
  - Intended to check **logical content equality** (e.g. `str1.equals(str2)`).
  - Must be explicitly overridden in custom classes, along with `hashCode()`.

```java
public class Main {
    public static void main(String[] args) {
        String s1 = new String("Java");
        String s2 = new String("Java");

        System.out.println("s1 == s2 (Memory references): " + (s1 == s2));       // FALSE
        System.out.println("s1.equals(s2) (Content equality): " + s1.equals(s2)); // TRUE
    }
}
```"""
    },

    "final_finally_finalize": {
        "title": "final vs finally vs finalize",
        "keywords": ["final vs finally", "final finally finalize", "difference between final and finally"],
        "content": """### ⚖️ `final` vs `finally` vs `finalize`

| Term | Category | Purpose |
|---|---|---|
| **`final`** | Keyword / Modifier | - Variables: Value cannot be reassigned (constants).<br>- Methods: Cannot be overridden.<br>- Classes: Cannot be subclassed/extended. |
| **`finally`** | Block (Exception Handling) | Block executed after `try-catch` regardless of whether an exception was thrown. Used for cleanup. |
| **`finalize()`** | Method (`java.lang.Object`) | Deprecated since Java 9. Formerly called before GC. Replaced by `AutoCloseable` and `java.lang.ref.Cleaner`. |

```java
final class ConstantConfig { // Cannot be extended
    final int MAX_USERS = 1000; // Cannot be reassigned
}

public class Main {
    public static void main(String[] args) {
        try {
            int result = 10 / 2;
            System.out.println("Result: " + result);
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            System.out.println("Finally block always executes!");
        }
    }
}
```"""
    },

    "throw_vs_throws": {
        "title": "throw vs throws in Java",
        "keywords": ["throw vs throws", "throws vs throw", "difference between throw and throws"],
        "content": """### ⚖️ `throw` vs `throws` in Java

| Feature | `throw` | `throws` |
|---|---|---|
| **Location** | Inside method or block body | In the **method signature** declaration |
| **Purpose** | Explicitly raises an exception object | Declares that a method might throw one or more exceptions |
| **Syntax** | Followed by an **instance** (`throw new IOException();`) | Followed by **exception class types** (`throws IOException, SQLException`) |
| **Quantity** | Can throw only **one** exception at a time | Can declare **multiple** comma-separated exceptions |

```java
public class Main {
    // 'throws' declares potential exceptions in signature
    static void checkAge(int age) throws IllegalArgumentException {
        if (age < 18) {
            // 'throw' explicitly creates and throws exception instance
            throw new IllegalArgumentException("Must be 18+ to enter!");
        }
        System.out.println("Access granted.");
    }

    public static void main(String[] args) {
        try {
            checkAge(15);
        } catch (IllegalArgumentException e) {
            System.out.println("Caught: " + e.getMessage());
        }
    }
}
```"""
    },

    "arraylist_vs_linkedlist": {
        "title": "ArrayList vs LinkedList",
        "keywords": ["arraylist vs linkedlist", "linkedlist vs arraylist"],
        "content": """### ⚖️ ArrayList vs LinkedList

| Feature | `ArrayList` | `LinkedList` |
|---|---|---|
| **Underlying Structure** | Resizable dynamic array | Doubly linked list |
| **Random Access `get(i)`** | **`O(1)`** (Direct memory index calculation) | **`O(n)`** (Must traverse nodes from head or tail) |
| **Insert/Delete in Middle** | `O(n)` (Requires shifting elements) | `O(1)` once position is found, `O(n)` to find |
| **Insert at End `add()`** | Amortized `O(1)` | `O(1)` |
| **Memory Overhead** | Low (contiguous array buffer) | High (Each node allocates `item`, `prev`, and `next` pointers) |
| **Implements** | `List`, `RandomAccess` | `List`, `Deque`, `Queue` |

> **Best Practice**: In 95%+ of production scenarios, **`ArrayList`** outperforms `LinkedList` due to CPU cache locality and zero node-pointer overhead!"""
    },

    "hashmap_vs_hashtable_concurrent": {
        "title": "HashMap vs Hashtable vs ConcurrentHashMap",
        "keywords": ["hashmap vs hashtable", "hashmap vs concurrenthashmap", "hashtable vs concurrenthashmap"],
        "content": """### ⚖️ HashMap vs Hashtable vs ConcurrentHashMap

| Feature | `HashMap` | `Hashtable` | `ConcurrentHashMap` |
|---|---|---|---|
| **Thread-Safe** | ❌ No | ✅ Yes (Locks entire map) | ✅ Yes (Lock-free reads, bucket-level locks) |
| **Null Keys / Values** | Allows 1 `null` key, multiple `null` values | ❌ No nulls allowed | ❌ No nulls allowed |
| **Performance** | Fastest for single thread | Slowest (Bottleneck on synchronized methods) | High concurrency throughput |
| **Legacy** | Modern (Java 1.2+) | Legacy (Avoid in new code) | Modern Concurrent utility (Java 1.5+) |"""
    },

    "pass_by_value": {
        "title": "Is Java Pass-by-Value or Pass-by-Reference?",
        "keywords": ["pass by value", "pass by reference", "is java pass by reference", "is java pass by value"],
        "content": """### 🔍 Is Java Pass-by-Value or Pass-by-Reference?

> **THE GOLDEN RULE**: **Java is strictly 100% Pass-by-Value at all times.**

#### The Confusion Explained:
- When you pass a primitive (`int`, `double`), a copy of the primitive value is passed.
- When you pass an **Object**, you are passing **a copy of the reference pointer** (memory address value).
  - You CAN mutate the object's internal fields through that copied reference.
  - You **CANNOT** reassign the caller's reference variable to point to a new object!

```java
class Person {
    String name;
    Person(String name) { this.name = name; }
}

public class Main {
    static void modify(Person p, int num) {
        num = 99;                 // Modifies local copy only
        p.name = "Alice";         // Modifies object through reference copy!
        p = new Person("Bob");    // Reassigns local copy of pointer only!
    }

    public static void main(String[] args) {
        int x = 10;
        Person person = new Person("Original");
        modify(person, x);

        System.out.println("x = " + x);                    // Still 10 (Primitive untouched)
        System.out.println("person.name = " + person.name); // "Alice" (Mutated)
        // NOT "Bob" because reassignment within method only altered the local pointer copy!
    }
}
```"""
    }
}

# Key Java Concepts & Deep Dive Answers
CONCEPTS = {
    "hashmap_internals": {
        "keywords": ["how hashmap works", "hashmap internal", "hashmap working", "hash collision", "load factor", "treeify"],
        "title": "Internal Working of HashMap in Java",
        "content": """### ⚙️ How HashMap Works Internally in Java

#### 1. Fundamental Structure
A `HashMap` uses an array of **Node buckets** (`Node<K,V>[] table`).
Each Node holds:
- `int hash` (Computed hash code of the key)
- `K key`
- `V value`
- `Node<K,V> next` (Pointer to next node for collision chaining)

#### 2. The `put(K key, V value)` Flow:
1. Calculates hash: `hash = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16)`.
2. Computes bucket index: `index = (n - 1) & hash` (Bitwise AND with table length - 1, extremely fast).
3. **If bucket is empty**: Places new node at `table[index]`.
4. **Collision Handling**:
   - If bucket has nodes, it traverses the linked list checking `p.hash == hash && ((k = p.key) == key || key.equals(k))`.
   - If key matches, value is replaced.
   - If end of list reached, appends new node.
5. **Java 8 Treeification Threshold (`TREEIFY_THRESHOLD = 8`)**:
   - If collisions in a single bucket reach **8 nodes** and total capacity >= 64, the linked list transforms into a **Red-Black Tree (`TreeNode`)**!
   - This improves lookup from `O(n)` to **`O(log n)`** during heavy collisions.
6. **Resizing & Load Factor (`DEFAULT_LOAD_FACTOR = 0.75`)**:
   - Default capacity = 16. Threshold = `16 * 0.75 = 12`.
   - When elements exceed 12, capacity doubles to 32 and rehashes."""
    },

    "constructors_chaining": {
        "keywords": ["constructor", "constructor chaining", "this()", "super()", "default constructor", "copy constructor"],
        "title": "Constructors and Constructor Chaining",
        "content": """### 🔨 Constructors & Constructor Chaining in Java

A **Constructor** is an initializer invoked during object creation with `new`.
- Has the exact same name as the class.
- Does **not** have any return type (not even `void`).
- If no constructor is written, the compiler provides an invisible **default no-arg constructor**.

#### Constructor Chaining:
- `this(...)`: Invokes another constructor in the **same class**.
- `super(...)`: Invokes the parent constructor.
- **Rule**: `this()` or `super()` must be the **very first statement** in the constructor body.

```java
class Account {
    private String id;
    private double balance;
    private String currency;

    public Account() {
        this("ACC-DEFAULT", 0.0); // Chaining to 2-arg
    }

    public Account(String id, double balance) {
        this(id, balance, "USD"); // Chaining to 3-arg
    }

    public Account(String id, double balance, String currency) {
        this.id = id;
        this.balance = balance;
        this.currency = currency;
    }

    @Override
    public String toString() {
        return "Account[" + id + ", balance=" + balance + " " + currency + "]";
    }

    public static void main(String[] args) {
        Account a1 = new Account();
        Account a2 = new Account("ACC-101", 500.0);
        System.out.println(a1);
        System.out.println(a2);
    }
}
```"""
    },

    "static_keyword": {
        "keywords": ["static keyword", "static method", "static variable", "static block", "method hiding"],
        "title": "The static Keyword in Java",
        "content": """### ⚡ The `static` Keyword in Java

The `static` modifier binds a member to the **class itself** rather than to individual instances.

#### Applications of `static`:
1. **Static Variables**: Single copy shared across all instances (stored in Metaspace/Class data). Great for counters and constants (`public static final`).
2. **Static Methods**: Can be invoked directly via `ClassName.methodName()`.
   - **Rule**: Cannot reference `this` or non-static instance fields directly.
3. **Static Blocks**: Executed once when the class is loaded by the ClassLoader.
4. **Static Nested Classes**: Nested classes that do not hold an implicit reference to an outer class instance.
5. **Method Hiding**: Static methods in a subclass do **not** override parent static methods; they *hide* them!

```java
public class Counter {
    private static int totalCreated = 0; // Shared static variable
    private int id;                       // Instance variable

    static {
        System.out.println("Counter class loaded into memory.");
    }

    public Counter() {
        totalCreated++;
        this.id = totalCreated;
    }

    public static int getTotalCreated() {
        return totalCreated;
    }

    public static void main(String[] args) {
        Counter c1 = new Counter();
        Counter c2 = new Counter();
        System.out.println("Total counters instantiated: " + Counter.getTotalCreated());
    }
}
```"""
    }
}

def find_best_answer(query: str) -> dict:
    """Intelligently matches query against comparisons, concepts, and topic curriculum using scored relevance."""
    lower_q = query.strip().lower()
    # Normalize punctuation and extra spaces
    normalized = re.sub(r'[^\w\s]', ' ', lower_q)
    tokens = set(normalized.split())

    best_match = None
    highest_score = 0

    # Helper to score candidate
    def evaluate_candidate(candidate_id, candidate_title, candidate_keywords, content_builder, code_snippet=""):
        score = 0

        # Exact phrase match in query
        for kw in candidate_keywords:
            kw_clean = kw.lower().strip()
            if kw_clean in lower_q:
                score += 15 + len(kw_clean)
            else:
                # Check token overlap
                kw_tokens = set(kw_clean.split())
                overlap = kw_tokens.intersection(tokens)
                if len(kw_tokens) > 1 and len(overlap) == len(kw_tokens):
                    score += 12 + len(kw_clean)
                elif overlap:
                    score += len(overlap) * 2

        # Check candidate title
        title_tokens = set(re.sub(r'[^\w\s]', ' ', candidate_title.lower()).split())
        title_overlap = title_tokens.intersection(tokens)
        score += len(title_overlap) * 3

        return score

    # 1. Evaluate Comparisons
    for key, item in COMPARISONS.items():
        s = evaluate_candidate(key, item["title"], item["keywords"], None)
        if s > highest_score and s >= 10:
            highest_score = s
            code = extract_java_code_from_markdown(item["content"])
            best_match = {
                "response": item["content"],
                "topic": key,
                "has_code": bool(code),
                "code_snippet": code
            }

    # 2. Evaluate Concepts
    for key, item in CONCEPTS.items():
        s = evaluate_candidate(key, item["title"], item["keywords"], None)
        if s > highest_score and s >= 10:
            highest_score = s
            code = extract_java_code_from_markdown(item["content"])
            best_match = {
                "response": item["content"],
                "topic": key,
                "has_code": bool(code),
                "code_snippet": code
            }

    # 3. Evaluate Curriculum Topics
    for key, topic in TOPICS_DATA.items():
        keywords = [key, key.replace("_", " "), topic["title"]]
        s = evaluate_candidate(key, topic["title"], keywords, None)
        if s > highest_score and s >= 10:
            highest_score = s
            resp = f"""### {topic['title']}\n\n**Category**: {topic['category']}\n\n{topic['details']}"""
            best_match = {
                "response": resp,
                "topic": key,
                "has_code": bool(topic.get("code")),
                "code_snippet": topic.get("code", "")
            }

    return best_match

def extract_java_code_from_markdown(markdown_text: str) -> str:
    """Extracts first Java code block from Markdown text."""
    match = re.search(r'```(?:java)?\n?([\s\S]*?)```', markdown_text)
    if match:
        return match.group(1).strip()
    return ""
