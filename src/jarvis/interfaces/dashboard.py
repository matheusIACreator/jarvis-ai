"""Loopback-only dashboard bridge; no outbound-action tools in the web chat."""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit


class Dashboard:
    def __init__(self, memory, reply, port=8765):
        self.memory, self.reply = memory, reply
        self.lock = threading.Lock()
        self.chat_lock = threading.Lock()
        self.state = {"phase": "starting", "messages": []}
        dashboard = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def respond(self, status, payload):
                body = json.dumps(payload, ensure_ascii=False).encode()
                try:
                    self.send_response(status)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
                    # The dashboard/proxy can cancel a request while we are replying.
                    # There is no client left to receive an error response or a retry.
                    self.close_connection = True

            def allowed(self):
                return self.headers.get("Host") == f"127.0.0.1:{dashboard.server.server_port}" and not self.headers.get("Origin")

            def do_GET(self):
                if not self.allowed():
                    return self.respond(403, {"error": "Forbidden"})
                url = urlsplit(self.path)
                if url.path == "/state":
                    with dashboard.lock:
                        state = {**dashboard.state, "messages": list(dashboard.state["messages"])}
                    # A slow/disconnected client must not hold up the voice loop.
                    return self.respond(200, state)
                if url.path == "/memory":
                    return self.respond(200, dashboard.memory.search(parse_qs(url.query).get("q", [""])[0]))
                self.respond(404, {"error": "Not found"})

            def do_POST(self):
                if not self.allowed():
                    return self.respond(403, {"error": "Forbidden"})
                if urlsplit(self.path).path != "/chat":
                    return self.respond(404, {"error": "Not found"})
                try:
                    size = int(self.headers.get("Content-Length", "0"))
                    if not 0 < size <= 20000:
                        return self.respond(413, {"error": "Invalid request size"})
                    text = json.loads(self.rfile.read(size)).get("text")
                    if not isinstance(text, str) or not text.strip() or len(text) > 4000:
                        return self.respond(400, {"error": "Invalid message"})
                except (ValueError, AttributeError):
                    return self.respond(400, {"error": "Invalid JSON"})
                if not dashboard.chat_lock.acquire(blocking=False):
                    return self.respond(409, {"error": "Jarvis is already answering"})
                try:
                    answer = dashboard.reply(text.strip())
                    self.respond(200, {"reply": answer})
                except Exception:
                    self.respond(503, {"error": "Unable to answer right now"})
                finally:
                    dashboard.chat_lock.release()

        self.server = ThreadingHTTPServer(("127.0.0.1", port), Handler)

    def phase(self, phase):
        with self.lock:
            self.state["phase"] = phase

    def message(self, role, text):
        with self.lock:
            self.state["messages"] = [*self.state["messages"], {"role": role, "text": text}][-30:]

    def start(self):
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
