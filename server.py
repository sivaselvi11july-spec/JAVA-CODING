#!/usr/bin/env python3
"""
Java Coding & OOP Chatbot Server.
Standard library HTTP server with REST APIs for:
- Chat engine & Java/OOP AI responses
- Real-time Java code compilation & execution (javac & java)
- Topic explorer and Interactive Quizzes
"""

import http.server
import json
import os
import sys
import subprocess
from urllib.parse import urlparse, parse_qs

# Import engine modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine.executor import run_java_code
from engine.oop_knowledge import answer_query, TOPICS
from engine.quiz_bank import get_all_quizzes, get_quizzes_by_topic

PORT = 8080
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

def get_java_version():
    try:
        res = subprocess.run(["javac", "-version"], capture_output=True, text=True, timeout=3)
        return (res.stdout.strip() or res.stderr.strip()) or "Unknown JDK"
    except Exception:
        return "JDK not detected"

class JavaChatbotHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def send_json(self, data, status=200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            self.send_json({
                "status": "online",
                "java": get_java_version(),
                "python": sys.version.split()[0],
                "port": PORT
            })
            return

        if path == "/api/topics":
            self.send_json(TOPICS)
            return

        if path == "/api/quiz":
            query_params = parse_qs(parsed.query)
            topic = query_params.get("topic", [None])[0]
            questions = get_quizzes_by_topic(topic)
            self.send_json({"questions": questions})
            return

        # Fallback to static file serving
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

        try:
            req_data = json.loads(body)
        except Exception:
            self.send_json({"error": "Invalid JSON body"}, status=400)
            return

        if path == "/api/chat":
            message = req_data.get("message", "")
            api_key = req_data.get("apiKey", "")
            
            if not message.strip():
                self.send_json({"error": "Message cannot be empty"}, status=400)
                return

            result = answer_query(message, api_key=api_key)
            self.send_json(result)
            return

        if path == "/api/run":
            code = req_data.get("code", "")
            stdin = req_data.get("stdin", "")
            if not code.strip():
                self.send_json({"error": "Code cannot be empty"}, status=400)
                return

            result = run_java_code(code, stdin_input=stdin)
            self.send_json(result)
            return

        self.send_json({"error": "Endpoint not found"}, status=404)

def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    server_address = ("", PORT)
    httpd = http.server.ThreadingHTTPServer(server_address, JavaChatbotHandler)
    print(f"[JavaCraft AI] Server running at http://localhost:{PORT}")
    print(f"[JavaCraft AI] Compiler status: {get_java_version()}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[JavaCraft AI] Shutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    main()
