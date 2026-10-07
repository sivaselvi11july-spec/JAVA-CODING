/**
 * JavaCraft AI - Interactive Java & OOP Assistant Frontend Logic
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const chatMessages = document.getElementById("chatMessages");
    const chatForm = document.getElementById("chatForm");
    const userInput = document.getElementById("userInput");
    const clearChatBtn = document.getElementById("clearChatBtn");
    const jdkVersionText = document.getElementById("jdkVersionText");
    const systemStatus = document.getElementById("systemStatus");
    
    // Playground Elements
    const playgroundSection = document.getElementById("playgroundSection");
    const togglePlaygroundBtn = document.getElementById("togglePlaygroundBtn");
    const closePlaygroundBtn = document.getElementById("closePlaygroundBtn");
    const codeEditor = document.getElementById("codeEditor");
    const runCodeBtn = document.getElementById("runCodeBtn");
    const loadSampleBtn = document.getElementById("loadSampleBtn");
    const formatCodeBtn = document.getElementById("formatCodeBtn");
    const consoleOutput = document.getElementById("consoleOutput");
    const execStatus = document.getElementById("execStatus");
    const execTime = document.getElementById("execTime");
    const clearConsoleBtn = document.getElementById("clearConsoleBtn");
    const currentFileName = document.getElementById("currentFileName");

    // Modals
    const topicsModal = document.getElementById("topicsModal");
    const toggleTopicsBtn = document.getElementById("toggleTopicsBtn");
    const closeTopicsBtn = document.getElementById("closeTopicsBtn");
    const topicsList = document.getElementById("topicsList");

    const quizModal = document.getElementById("quizModal");
    const toggleQuizBtn = document.getElementById("toggleQuizBtn");
    const closeQuizBtn = document.getElementById("closeQuizBtn");
    const quizCard = document.getElementById("quizCard");
    const nextQuizBtn = document.getElementById("nextQuizBtn");
    const quizScoreBadge = document.getElementById("quizScoreBadge");

    const settingsModal = document.getElementById("settingsModal");
    const settingsBtn = document.getElementById("settingsBtn");
    const closeSettingsBtn = document.getElementById("closeSettingsBtn");
    const geminiApiKeyInput = document.getElementById("geminiApiKey");
    const saveSettingsBtn = document.getElementById("saveSettingsBtn");
    const detectedJavaInfo = document.getElementById("detectedJavaInfo");

    const themeToggleBtn = document.getElementById("themeToggleBtn");
    const themeIcon = document.getElementById("themeIcon");

    // State Variables
    let currentQuizIndex = 0;
    let quizQuestions = [];
    let quizScore = 0;
    let quizTotalAnswered = 0;
    let isPlaygroundOpen = true;

    // Default Java Playground Template
    const DEFAULT_JAVA_CODE = `// Java 23 OOP Demonstration
// Dynamic Method Dispatch & Polymorphism
abstract class Animal {
    protected String name;

    public Animal(String name) {
        this.name = name;
    }

    public abstract void makeSound();
}

class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }

    @Override
    public void makeSound() {
        System.out.println(name + " says: Woof! Woof! 🐶");
    }
}

class Cat extends Animal {
    public Cat(String name) {
        super(name);
    }

    @Override
    public void makeSound() {
        System.out.println(name + " says: Meow! 🐱");
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println("=== Java 23 OOP Demo ===");
        
        Animal[] pets = {
            new Dog("Buddy"),
            new Cat("Luna")
        };

        for (Animal pet : pets) {
            pet.makeSound(); // Dynamic Binding at Runtime
        }
    }
}`;

    // Initialize Code Editor
    codeEditor.value = DEFAULT_JAVA_CODE;

    // 1. Check Server & JDK Status
    async function checkServerStatus() {
        try {
            const res = await fetch("/api/status");
            const data = await res.json();
            jdkVersionText.textContent = `${data.java} Ready`;
            detectedJavaInfo.textContent = `${data.java} (Port ${data.port})`;
            systemStatus.querySelector(".status-dot").style.backgroundColor = "var(--success)";
        } catch (e) {
            jdkVersionText.textContent = "Offline / Connection Error";
            systemStatus.querySelector(".status-dot").style.backgroundColor = "var(--error)";
        }
    }
    checkServerStatus();

    // 2. Tab key support in Code Editor
    codeEditor.addEventListener("keydown", (e) => {
        if (e.key === "Tab") {
            e.preventDefault();
            const start = codeEditor.selectionStart;
            const end = codeEditor.selectionEnd;
            codeEditor.value = codeEditor.value.substring(0, start) + "    " + codeEditor.value.substring(end);
            codeEditor.selectionStart = codeEditor.selectionEnd = start + 4;
        }
    });

    // 3. User Input Auto-resize & Shift+Enter support
    userInput.addEventListener("input", () => {
        userInput.style.height = "auto";
        userInput.style.height = Math.min(userInput.scrollHeight, 140) + "px";
    });

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event("submit"));
        }
    });

    // 4. Chat Submission
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (!text) return;

        // Hide welcome card if present
        const welcomeCard = document.getElementById("welcomeCard");
        if (welcomeCard) welcomeCard.style.display = "none";

        // Add user message to UI
        appendMessage("user", text);
        userInput.value = "";
        userInput.style.height = "auto";

        // Show typing indicator
        const typingId = appendTypingIndicator();

        // Call backend API
        try {
            const apiKey = localStorage.getItem("javacraft_gemini_api_key") || "";
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text, apiKey })
            });
            const data = await response.json();
            removeTypingIndicator(typingId);

            if (data.error) {
                appendMessage("bot", `⚠️ **Error**: ${data.error}`);
            } else {
                appendMessage("bot", data.response);
                // If code is returned, update Playground if empty
                if (data.code_snippet && !codeEditor.value.trim()) {
                    loadCodeIntoPlayground(data.code_snippet);
                }
            }
        } catch (err) {
            removeTypingIndicator(typingId);
            appendMessage("bot", "⚠️ Could not connect to the JavaCraft assistant server. Please verify the server is running.");
        }
    });

    // Quick prompt chip click handler
    document.addEventListener("click", (e) => {
        const chip = e.target.closest(".prompt-chip");
        if (chip) {
            const query = chip.getAttribute("data-query");
            if (query) {
                userInput.value = query;
                chatForm.dispatchEvent(new Event("submit"));
            }
        }
    });

    // 5. Append Chat Messages & Rich Markdown Rendering
    function appendMessage(sender, content) {
        const bubble = document.createElement("div");
        bubble.className = `message-bubble ${sender}`;

        const avatar = document.createElement("div");
        avatar.className = "message-avatar";
        avatar.innerHTML = sender === "user" ? "👤" : "☕";

        const body = document.createElement("div");
        body.className = "message-body";

        if (sender === "user") {
            body.textContent = content;
        } else {
            body.innerHTML = parseMarkdownToHtml(content);
            attachCodeBlockActions(body);
        }

        bubble.appendChild(avatar);
        bubble.appendChild(body);
        chatMessages.appendChild(bubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendTypingIndicator() {
        const id = "typing-" + Date.now();
        const bubble = document.createElement("div");
        bubble.className = "message-bubble bot";
        bubble.id = id;
        bubble.innerHTML = `
            <div class="message-avatar">☕</div>
            <div class="message-body">
                <span class="typing-dots">Thinking & compiling OOP response...</span>
            </div>
        `;
        chatMessages.appendChild(bubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    // Markdown Parser
    function parseMarkdownToHtml(markdown) {
        let html = markdown;

        // Escape dangerous HTML tags except our own formatting
        html = html.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

        // Code blocks: ```java ... ```
        html = html.replace(/```(?:java)?\n?([\s\S]*?)```/g, (match, code) => {
            const unescapedCode = code
                .replace(/&amp;/g, "&")
                .replace(/&lt;/g, "<")
                .replace(/&gt;/g, ">");
            
            return `<div class="code-block-container">
                <div class="code-header">
                    <span>Java Source</span>
                    <div class="code-header-actions">
                        <button class="code-action-btn copy-btn" data-code="${encodeURIComponent(unescapedCode)}">📋 Copy</button>
                        <button class="code-action-btn primary run-sandbox-btn" data-code="${encodeURIComponent(unescapedCode)}">▶ Run in Playground</button>
                    </div>
                </div>
                <pre><code>${code.trim()}</code></pre>
            </div>`;
        });

        // Inline code `code`
        html = html.replace(/`([^`]+)`/g, "<code>$1</code>");

        // Headings: ### and ####
        html = html.replace(/^### (.*$)/gim, "<h3>$1</h3>");
        html = html.replace(/^#### (.*$)/gim, "<h4>$1</h4>");

        // Bold: **text**
        html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

        // Blockquotes: > quote
        html = html.replace(/^> (.*$)/gim, "<blockquote>$1</blockquote>");

        // Bullet lists: - or *
        html = html.replace(/^\s*[-*]\s+(.*$)/gim, "<li>$1</li>");
        html = html.replace(/(<li>.*<\/li>)/gim, "<ul>$1</ul>");

        // Tables parsing: basic table structure
        html = html.replace(/\|(.+)\|/gim, (match) => {
            if (match.includes("---")) return ""; // Skip separator
            const cells = match.split("|").slice(1, -1).map(c => `<td>${c.trim()}</td>`).join("");
            return `<tr>${cells}</tr>`;
        });
        html = html.replace(/(<tr>.*<\/tr>)+/gim, "<table>$1</table>");

        // Line breaks (paragraph separation)
        html = html.replace(/\n\n/g, "<p></p>");

        return html;
    }

    // Attach Copy and Run buttons on generated code blocks
    function attachCodeBlockActions(container) {
        container.querySelectorAll(".copy-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const code = decodeURIComponent(btn.getAttribute("data-code"));
                navigator.clipboard.writeText(code);
                const oldText = btn.textContent;
                btn.textContent = "✓ Copied!";
                setTimeout(() => btn.textContent = oldText, 2000);
            });
        });

        container.querySelectorAll(".run-sandbox-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const code = decodeURIComponent(btn.getAttribute("data-code"));
                loadCodeIntoPlayground(code);
                if (playgroundSection.classList.contains("hidden")) {
                    togglePlayground(true);
                }
                executeJavaCode();
            });
        });
    }

    function loadCodeIntoPlayground(code) {
        codeEditor.value = code;
        // Extract class name for header tab
        const match = code.match(/\b(?:public\s+)?(?:class|record)\s+([A-Za-z0-9_$]+)/);
        if (match && match[1]) {
            currentFileName.textContent = `${match[1]}.java`;
        } else {
            currentFileName.textContent = "Main.java";
        }
    }

    // 6. Java Code Execution Engine
    async function executeJavaCode() {
        const code = codeEditor.value;
        if (!code.trim()) {
            alert("Please write or paste Java code first.");
            return;
        }

        execStatus.className = "exec-badge running";
        execStatus.textContent = "Compiling & Running...";
        execTime.textContent = "";
        consoleOutput.innerHTML = `<pre style="color: var(--warning);">⚡ Invoking javac & java (Java 23)...</pre>`;
        runCodeBtn.disabled = true;

        try {
            const res = await fetch("/api/run", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code })
            });
            const data = await res.json();
            runCodeBtn.disabled = false;

            if (data.executionTimeMs !== undefined) {
                execTime.textContent = `${data.executionTimeMs} ms`;
            }

            if (data.success) {
                execStatus.className = "exec-badge success";
                execStatus.textContent = "Success";
                const stdoutText = data.stdout || "(Program finished with no output to stdout)";
                consoleOutput.innerHTML = `<pre class="stdout">${escapeHtml(stdoutText)}</pre>`;
            } else if (!data.compiled) {
                execStatus.className = "exec-badge error";
                execStatus.textContent = "Compile Error";
                consoleOutput.innerHTML = `<pre class="stderr">❌ Compilation Error:\n${escapeHtml(data.stderr || data.error)}</pre>`;
            } else {
                execStatus.className = "exec-badge error";
                execStatus.textContent = "Runtime Error";
                consoleOutput.innerHTML = `<pre class="stderr">⚠️ Runtime Exception / Error (Exit code ${data.exitCode}):\n${escapeHtml(data.stderr || data.error)}</pre>`;
            }
        } catch (err) {
            runCodeBtn.disabled = false;
            execStatus.className = "exec-badge error";
            execStatus.textContent = "Failed";
            consoleOutput.innerHTML = `<pre class="stderr">Network or Server Error: Could not connect to Java runtime service.</pre>`;
        }
    }

    runCodeBtn.addEventListener("click", executeJavaCode);

    clearConsoleBtn.addEventListener("click", () => {
        consoleOutput.innerHTML = "<pre>Console cleared.</pre>";
        execStatus.className = "exec-badge";
        execStatus.textContent = "Ready";
        execTime.textContent = "";
    });

    loadSampleBtn.addEventListener("click", () => {
        loadCodeIntoPlayground(DEFAULT_JAVA_CODE);
    });

    formatCodeBtn.addEventListener("click", () => {
        codeEditor.value = `public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, Java 23!");\n    }\n}`;
        currentFileName.textContent = "Main.java";
    });

    // 7. Playground Toggle
    function togglePlayground(show) {
        if (show === undefined) {
            isPlaygroundOpen = !isPlaygroundOpen;
        } else {
            isPlaygroundOpen = show;
        }

        if (isPlaygroundOpen) {
            playgroundSection.classList.remove("hidden");
            togglePlaygroundBtn.classList.add("primary");
        } else {
            playgroundSection.classList.add("hidden");
            togglePlaygroundBtn.classList.remove("primary");
        }
    }

    togglePlaygroundBtn.addEventListener("click", () => togglePlayground());
    closePlaygroundBtn.addEventListener("click", () => togglePlayground(false));

    // 8. Topics Curriculum Modal
    let allLoadedTopics = null;
    const topicSearchInput = document.getElementById("topicSearchInput");

    toggleTopicsBtn.addEventListener("click", async () => {
        topicsModal.classList.add("active");
        if (!allLoadedTopics) {
            try {
                const res = await fetch("/api/topics");
                allLoadedTopics = await res.json();
                renderTopics(allLoadedTopics);
            } catch (e) {
                topicsList.innerHTML = "<p>Failed to load curriculum topics.</p>";
            }
        }
    });

    closeTopicsBtn.addEventListener("click", () => topicsModal.classList.remove("active"));
    topicsModal.addEventListener("click", (e) => {
        if (e.target === topicsModal) topicsModal.classList.remove("active");
    });

    if (topicSearchInput) {
        topicSearchInput.addEventListener("input", (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (!allLoadedTopics) return;
            const filtered = {};
            for (const [key, t] of Object.entries(allLoadedTopics)) {
                const titleMatch = (t.title || "").toLowerCase().includes(query);
                const catMatch = (t.category || "").toLowerCase().includes(query);
                const sumMatch = (t.summary || "").toLowerCase().includes(query);
                if (titleMatch || catMatch || sumMatch) {
                    filtered[key] = t;
                }
            }
            renderTopics(filtered);
        });
    }

    function renderTopics(topics) {
        topicsList.innerHTML = "";
        const keys = Object.keys(topics);
        if (keys.length === 0) {
            topicsList.innerHTML = "<p style='color: var(--text-muted); text-align: center; padding: 20px;'>No matching Java topics found.</p>";
            return;
        }

        // Group by category if present
        const groups = {};
        for (const [key, t] of Object.entries(topics)) {
            const cat = t.category || "General Java & OOP";
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push({ key, ...t });
        }

        for (const [categoryName, items] of Object.entries(groups)) {
            const groupHeader = document.createElement("div");
            groupHeader.style.cssText = "font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: var(--accent); letter-spacing: 0.5px; margin: 16px 0 8px 0;";
            groupHeader.textContent = categoryName;
            topicsList.appendChild(groupHeader);

            for (const itemData of items) {
                const item = document.createElement("div");
                item.className = "topic-item";
                item.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <h4 style="margin: 0 0 4px 0;">${itemData.title}</h4>
                        <span style="font-size: 0.72rem; color: var(--java-orange); font-weight: 600;">Runnable</span>
                    </div>
                    <p>${itemData.summary || itemData.description || ""}</p>
                `;
                item.addEventListener("click", () => {
                    topicsModal.classList.remove("active");
                    if (itemData.code) {
                        loadCodeIntoPlayground(itemData.code);
                        if (playgroundSection.classList.contains("hidden")) togglePlayground(true);
                    }
                    userInput.value = `Explain ${itemData.title} in Java with concepts and examples`;
                    chatForm.dispatchEvent(new Event("submit"));
                });
                topicsList.appendChild(item);
            }
        }
    }

    // 9. Interactive Quiz Modal
    toggleQuizBtn.addEventListener("click", async () => {
        quizModal.classList.add("active");
        if (quizQuestions.length === 0) {
            try {
                const res = await fetch("/api/quiz");
                const data = await res.json();
                quizQuestions = data.questions || [];
                currentQuizIndex = 0;
                quizScore = 0;
                quizTotalAnswered = 0;
                updateQuizScore();
                renderQuizQuestion();
            } catch (e) {
                quizCard.innerHTML = "<p>Error loading quiz questions.</p>";
            }
        } else {
            renderQuizQuestion();
        }
    });

    closeQuizBtn.addEventListener("click", () => quizModal.classList.remove("active"));
    quizModal.addEventListener("click", (e) => {
        if (e.target === quizModal) quizModal.classList.remove("active");
    });

    function updateQuizScore() {
        quizScoreBadge.textContent = `Score: ${quizScore} / ${quizTotalAnswered}`;
    }

    function renderQuizQuestion() {
        if (quizQuestions.length === 0) return;
        const q = quizQuestions[currentQuizIndex];

        quizCard.innerHTML = `
            <div class="quiz-meta">
                <span><strong>Topic:</strong> ${q.topic}</span>
                <span><strong>Difficulty:</strong> ${q.difficulty}</span>
            </div>
            <div class="quiz-question-text">${q.question}</div>
            ${q.code ? `<div class="quiz-code-box"><pre><code>${escapeHtml(q.code)}</code></pre></div>` : ""}
            <div class="quiz-options">
                ${q.options.map((opt, idx) => `
                    <button class="quiz-option-btn" data-idx="${idx}">
                        <strong>${String.fromCharCode(65 + idx)}.</strong> ${escapeHtml(opt)}
                    </button>
                `).join("")}
            </div>
            <div class="quiz-explanation" id="quizExplanation" style="display: none;">
                <strong>Explanation:</strong> ${escapeHtml(q.explanation)}
            </div>
        `;

        // Handle answer selection
        const optionBtns = quizCard.querySelectorAll(".quiz-option-btn");
        let answered = false;

        optionBtns.forEach(btn => {
            btn.addEventListener("click", () => {
                if (answered) return;
                answered = true;
                const selectedIdx = parseInt(btn.getAttribute("data-idx"));
                quizTotalAnswered++;

                if (selectedIdx === q.correct) {
                    btn.classList.add("correct");
                    btn.innerHTML += " ✓ Correct!";
                    quizScore++;
                } else {
                    btn.classList.add("wrong");
                    btn.innerHTML += " ✗";
                    optionBtns[q.correct].classList.add("correct");
                }

                optionBtns.forEach(b => b.disabled = true);
                updateQuizScore();
                document.getElementById("quizExplanation").style.display = "block";
            });
        });
    }

    nextQuizBtn.addEventListener("click", () => {
        currentQuizIndex = (currentQuizIndex + 1) % quizQuestions.length;
        renderQuizQuestion();
    });

    // 10. Settings & API Key
    settingsBtn.addEventListener("click", () => {
        settingsModal.classList.add("active");
        geminiApiKeyInput.value = localStorage.getItem("javacraft_gemini_api_key") || "";
    });

    closeSettingsBtn.addEventListener("click", () => settingsModal.classList.remove("active"));
    settingsModal.addEventListener("click", (e) => {
        if (e.target === settingsModal) settingsModal.classList.remove("active");
    });

    saveSettingsBtn.addEventListener("click", () => {
        const key = geminiApiKeyInput.value.trim();
        if (key) {
            localStorage.setItem("javacraft_gemini_api_key", key);
        } else {
            localStorage.removeItem("javacraft_gemini_api_key");
        }
        settingsModal.classList.remove("active");
    });

    // 11. Theme Toggle
    const savedTheme = localStorage.getItem("javacraft_theme") || "dark";
    if (savedTheme === "light") {
        document.body.classList.replace("dark-theme", "light-theme");
        themeIcon.textContent = "🌙";
    }

    themeToggleBtn.addEventListener("click", () => {
        if (document.body.classList.contains("dark-theme")) {
            document.body.classList.replace("dark-theme", "light-theme");
            themeIcon.textContent = "🌙";
            localStorage.setItem("javacraft_theme", "light");
        } else {
            document.body.classList.replace("light-theme", "dark-theme");
            themeIcon.textContent = "☀️";
            localStorage.setItem("javacraft_theme", "dark");
        }
    });

    // 12. Clear Chat History
    clearChatBtn.addEventListener("click", () => {
        chatMessages.innerHTML = `
            <div class="welcome-card" id="welcomeCard">
                <div class="welcome-avatar">☕</div>
                <h2>Chat Cleared</h2>
                <p>Ready for your next Java or OOP question.</p>
                <div class="quick-prompts">
                    <button class="prompt-chip" data-query="Explain the 4 Pillars of OOP in Java with real-world examples">🌟 4 Pillars of OOP</button>
                    <button class="prompt-chip" data-query="Explain Polymorphism: Overloading vs Overriding with code">🎭 Polymorphism</button>
                    <button class="prompt-chip" data-query="What is the difference between Abstract Class and Interface in modern Java?">⚖️ Abstract vs Interface</button>
                </div>
            </div>
        `;
    });

    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
