"""
Java Coding and Object-Oriented Programming (OOP) Knowledge Engine.
Connects topics, comparison matrix, deep architectural concepts, and static code diagnostics.
"""

import re
import urllib.request
import json
import os

from engine.topics_data import TOPICS_DATA
from engine.knowledge_base import find_best_answer, COMPARISONS, CONCEPTS

# Export TOPICS for the server and frontend
TOPICS = TOPICS_DATA

def analyze_user_code(code_str: str) -> str:
    """Provides automated static OOP feedback, bug diagnosis, and best practice checks on Java code."""
    issues = []
    suggestions = []
    
    # Check for class or interface definition
    if not re.search(r'\b(class|record|interface|enum)\b', code_str):
        suggestions.append("• **Class Structure**: No class or interface declaration found. Java requires code inside a class, record, or interface.")
        
    # Check for main method
    if "public static void main" not in code_str:
        suggestions.append("• **Entry Point**: No `public static void main(String[] args)` method detected. To run standalone in the playground, add a main method.")
        
    # Check for public field anti-pattern (Encapsulation violation)
    public_fields = re.findall(r'public\s+(?:int|double|String|boolean|float|long|char)\s+([a-zA-Z0-9_]+)\s*;', code_str)
    if public_fields:
        issues.append(f"• **Encapsulation Alert**: Detected public instance field(s): `{', '.join(public_fields)}`. Practice Data Hiding by making fields `private` and exposing getters/setters with validation.")
        
    # Check for missing @Override in inheritance
    if re.search(r'class\s+\w+\s+extends\s+\w+', code_str):
        if "@Override" not in code_str and ("void " in code_str or "String " in code_str):
            suggestions.append("• **Polymorphism Best Practice**: When overriding methods from a superclass, annotate them with `@Override` to catch method signature typos at compile time.")

    # Check for String == comparison
    if re.search(r'["\w]+\s*==\s*["\w]+', code_str) and "String" in code_str:
        if '==' in code_str and '"' in code_str:
            issues.append("• **String Comparison Pitfall**: Detected `==` with Strings. In Java, `==` tests object reference equality (memory addresses). Always use `.equals()` for content equality!")

    # Check for equals() without hashCode()
    has_equals = "boolean equals(Object" in code_str or "boolean equals(" in code_str
    has_hashcode = "int hashCode()" in code_str
    if has_equals and not has_hashcode:
        issues.append("• **Object Contract Violation**: Found `equals()` without overriding `hashCode()`. This will cause bugs when storing instances in `HashMap` or `HashSet`.")

    # Check for empty catch block (exception swallowing)
    if re.search(r'catch\s*\([^)]+\)\s*\{\s*\}', code_str):
        issues.append("• **Exception Swallowing**: Empty `catch` block detected! Never silently swallow exceptions—log them or rethrow to preserve debugging information.")

    # Check for raw types in collections
    if re.search(r'\b(List|ArrayList|Set|HashSet|Map|HashMap)\s+[a-zA-Z0-9_]+\s*=', code_str):
        if "<" not in code_str:
            suggestions.append("• **Generics & Type Safety**: Detected raw collection types. Specify generic parameters (e.g. `List<String> list = new ArrayList<>()`) to prevent `ClassCastException`.")

    # Check for Optional.get() without isPresent()
    if ".get()" in code_str and "Optional" in code_str:
        suggestions.append("• **Optional Anti-Pattern**: Avoid direct `.get()` on `Optional`. Prefer `.orElse()`, `.orElseGet()`, or `.ifPresent()` to avoid `NoSuchElementException`.")

    feedback_parts = ["### 🔍 Static Code Review & OOP Diagnosis\n"]
    if issues:
        feedback_parts.append("**⚠️ Critical Issues & OOP Violations:**\n" + "\n".join(issues) + "\n")
    if suggestions:
        feedback_parts.append("**💡 Best Practice Suggestions:**\n" + "\n".join(suggestions) + "\n")
    if not issues and not suggestions:
        feedback_parts.append("✨ **Great job!** The syntax and structure follow clean Java OOP conventions. Click **'Run in Playground'** to compile and run it live.")

    return "\n".join(feedback_parts)

def call_gemini_api_if_configured(prompt: str, api_key: str = None) -> str:
    """Optional external LLM call if user supplies an API key."""
    key = api_key or os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    payload = {
        "contents": [{
            "parts": [{
                "text": f"You are an expert Java coding and Object-Oriented Programming (OOP) master tutor. Answer thoroughly with clear Java code examples and OOP principles.\n\nUser Question:\n{prompt}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2000
        }
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=12) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return None

def answer_query(query: str, api_key: str = None) -> dict:
    """Processes any user query against the comprehensive Java & OOP repository."""
    cleaned = query.strip()
    lower_q = cleaned.lower()
    
    # 1. Code Review & Debugging (User pasted Java code)
    if ("public class " in cleaned or "class " in cleaned or "public static void main" in cleaned) and len(cleaned) > 40:
        review = analyze_user_code(cleaned)
        return {
            "response": review,
            "topic": "code_review",
            "has_code": True,
            "code_snippet": cleaned
        }

    # 2. Query Knowledge Base (Comparisons, Concepts, Topics)
    kb_result = find_best_answer(query)
    if kb_result:
        return kb_result

    # 3. Four Pillars General Inquiry
    if any(k in lower_q for k in ["what is oop", "oops concept", "oop concept", "explain oop", "object oriented programming", "pillars"]):
        resp = """### 🌟 Object-Oriented Programming (OOP) in Java

**Object-Oriented Programming (OOP)** is the cornerstone software paradigm built around **Objects** containing data (attributes/fields) and behaviors (methods/functions).

#### The 4 Core Pillars of OOP:
1. **🛡️ Encapsulation**: Restricting direct access to an object's internal fields by keeping variables `private` and exposing controlled `public` getters/setters with validation.
2. **🧬 Inheritance**: Creating new classes based on existing ones (`extends`) to foster code reusability and hierarchical categorization.
3. **🎭 Polymorphism**: Enabling an entity to take multiple forms—either at compile-time (**Method Overloading**) or at runtime (**Method Overriding** via Dynamic Method Dispatch).
4. **🧩 Abstraction**: Hiding complex internal implementation details and exposing only essential contracts using **Abstract Classes** and **Interfaces**.

#### Advanced OOP & Java Principles:
- **SOLID Design Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.
- **GoF Design Patterns**: Singleton, Factory, Builder, Strategy, Observer, Decorator.
- **Memory & Lifecycle**: Stack vs Heap, Metaspace, Generational GC, the `equals()` & `hashCode()` contract.
- **Modern Java Primitives**: `record` (immutable data carriers), `sealed` classes, Virtual Threads (Java 21).

*Ask me about any specific topic or click a Quick Starter chip below!*"""
        return {
            "response": resp,
            "topic": "four_pillars",
            "has_code": True,
            "code_snippet": TOPICS_DATA["polymorphism"]["code"]
        }

    # 4. Optional Gemini Fallback
    if api_key:
        llm_resp = call_gemini_api_if_configured(query, api_key)
        if llm_resp:
            return {
                "response": llm_resp,
                "topic": "ai_response",
                "has_code": "```java" in llm_resp,
                "code_snippet": ""
            }

    # 5. Fallback Guide with Extensive Suggestions
    default_resp = f"""### ☕ JavaCraft Knowledge Engine

I didn't find an exact pre-indexed match for **"{cleaned}"**, but I have deep knowledge across all Java & OOP disciplines. You can ask me about:

- **The 4 Pillars**: Encapsulation, Inheritance, Polymorphism, Abstraction
- **Architectural Design**: SOLID Principles, Composition vs Inheritance, Law of Demeter
- **Design Patterns**: Singleton (Bill Pugh & Enum), Builder, Factory, Strategy, Observer
- **Core Comparisons**: Abstract Class vs Interface, Overloading vs Overriding, `==` vs `.equals()`, String vs StringBuilder vs StringBuffer, Comparable vs Comparator
- **Java Internals & Memory**: How HashMap works internally, Stack vs Heap, Generational GC, Pass-by-value proof
- **Collections & Generics**: ArrayList vs LinkedList, HashMap treeification, PECS rule (`? extends` / `? super`)
- **Modern Java (Java 8 to 23)**: Streams & Lambdas, Optional, Records, Sealed classes, Virtual Threads (Project Loom)
- **Code Review**: Paste any Java snippet here to debug and inspect OOP violations!
- **Interactive Quiz**: Click **"🧠 Quiz Mode"** in the top bar to test your skills!

*Try: "How does HashMap work internally?" or "Explain the Builder pattern in Java"*"""
    return {
        "response": default_resp,
        "topic": "general",
        "has_code": False,
        "code_snippet": ""
    }
