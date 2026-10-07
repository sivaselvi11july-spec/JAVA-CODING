"""
Vercel Serverless Entrypoint for JavaCraft AI.
Handles API routing for:
- /api/chat
- /api/run
- /api/status
- /api/topics
- /api/quiz
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from urllib.parse import urlparse, parse_qs

# Ensure engine package is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from engine.executor import run_java_code
from engine.oop_knowledge import answer_query, TOPICS
from engine.quiz_bank import get_all_quizzes, get_quizzes_by_topic

class handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def normalize_path(self, path):
        # Handle rewrites where path might be /api/topics or /api/index?path=...
        if "/api/status" in path:
            return "/api/status"
        if "/api/topics" in path:
            return "/api/topics"
        if "/api/quiz" in path:
            return "/api/quiz"
        if "/api/chat" in path:
            return "/api/chat"
        if "/api/run" in path:
            return "/api/run"
        return path

    def do_GET(self):
        parsed = urlparse(self.path)
        path = self.normalize_path(parsed.path)

        if path == "/api/status":
            self.send_json({
                "status": "online",
                "java": "Cloud Sandbox / Vercel Serverless",
                "environment": "Vercel",
                "port": 443
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

        self.send_json({"error": "Endpoint not found", "path": self.path}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = self.normalize_path(parsed.path)

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

        self.send_json({"error": "Endpoint not found", "path": self.path}, status=404)
