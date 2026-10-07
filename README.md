# ☕ JavaCraft AI: Java Coding & OOP Chatbot

An intelligent, interactive assistant and coding sandbox tailored specifically for **Java programming** and **Object-Oriented Programming (OOP) concepts**.

Built with a native Python 3 standard library backend and modern responsive frontend, connecting directly to your installed **Java 23 JDK** for real-time compilation and execution.

---

## 🌟 Key Features

### 1. 🤖 Intelligent Java & OOP Assistant
- **The 4 Pillars of OOP**: Deep explanations, best practices, real-world analogies, and runnable code for **Encapsulation**, **Inheritance**, **Polymorphism**, and **Abstraction**.
- **SOLID Design Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion explained with Java before/after code.
- **Design Patterns in Java**: Creational (Singleton, Builder, Factory), Behavioral (Strategy, Observer), and Structural patterns.
- **Abstract Classes vs. Interfaces**: Evolution from traditional interfaces to Java 8+ `default`/`static` methods and Java 9+ `private` methods.
- **Memory Architecture & JVM**: Stack vs. Heap allocation, Generational Garbage Collection, Metaspace, and the `equals()` & `hashCode()` contract.
- **Modern Java Features**: Java 16+ `record` classes, Java 17+ `sealed` classes and interfaces, Java 21+ Pattern Matching for `switch`.

### 2. ⚡ Live Java 23 Code Playground & Sandbox
- Instant in-browser Java sandbox powered by the local `javac` and `java` runtime.
- Click **"▶ Run in Playground"** on any code snippet returned by the chatbot to test it live with one click.
- Terminal output view displaying compilation errors (`javac`), runtime exceptions, standard output, and execution time in milliseconds.
- Built-in infinite loop & timeout safety guard (8-second threshold).

### 3. 🔍 Static Code Review & Bug Explainer
- Paste any Java snippet into the chat to get instant static analysis:
  - Encapsulation checks (detects unencapsulated `public` instance fields).
  - String equality traps (`==` vs `.equals()`).
  - Raw collection types (suggests generics `<T>`).
  - Missing `@Override` annotations in inheritance hierarchies.

### 4. 🧠 Interactive OOP Quiz Mode
- Multiple-choice questions (MCQs) and output-prediction challenges covering dynamic dispatch, inheritance rules, access modifiers, and SOLID patterns.
- Instant feedback with correct/incorrect highlights, live score tracker, and in-depth conceptual explanations.

### 5. 📚 Guided Curriculum Explorer
- Quick-access drawer with curated learning topics and one-click code loading into the sandbox.

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** (Uses standard library, **zero `pip` dependencies required**)
- **JDK 17+** (Java 23 is already detected on this system)

### Running the Application

1. Open PowerShell or Command Prompt in the project folder:
   ```powershell
   cd C:\Users\Student\.gemini\antigravity\scratch\java-oop-chatbot
   ```

2. Start the server using either launcher:
   - **Double-click** `run.bat`
   - Or run with PowerShell:
     ```powershell
     .\run.ps1
     ```
   - Or run with Python directly:
     ```powershell
     python server.py
     ```

3. Open your browser at:
   ```
   http://localhost:8080
   ```

---

## 📁 Project Structure

```
java-oop-chatbot/
├── server.py              # HTTP server & REST APIs (/api/chat, /api/run, /api/topics, /api/quiz)
├── engine/
│   ├── __init__.py
│   ├── executor.py        # Compiles and runs Java code via javac and java safely
│   ├── oop_knowledge.py   # Curated Java & OOP knowledge engine, code templates & static analyzer
│   └── quiz_bank.py       # Rich collection of interview & conceptual OOP quiz questions
├── static/
│   ├── index.html         # Modern web interface (Chat + Java Sandbox split view)
│   ├── style.css          # Dark/Light responsive UI styling
│   └── app.js             # Frontend reactive application logic
├── run.bat                # Windows 1-click batch launcher
├── run.ps1                # PowerShell launcher script
└── README.md              # Project documentation
```

---

## 💡 Example Queries to Try in Chat

- *"Explain the 4 Pillars of OOP with real-world analogies and Java code."*
- *"What is the difference between Method Overloading and Method Overriding?"*
- *"How does the Liskov Substitution Principle work in Java?"*
- *"Why must I override hashCode() when overriding equals()?"*
- *"Show me an implementation of the Builder Pattern in Java."*
- *"What are sealed classes and records in modern Java?"*
- Paste your own Java class to inspect OOP design and debug issues!
