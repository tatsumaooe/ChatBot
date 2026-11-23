"""
Web chat server for ChatBot.

Run from the project root:

    python -m model.server            # then open http://localhost:8000
    python -m model.server --open     # also opens your browser
    python -m model.server --host 0.0.0.0 --port 8080   # reachable on your network

Uses only the Python standard library (no Flask etc. needed).
"""

import argparse
import json
import threading
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from model.chat import respond


WEB_DIR = Path(__file__).resolve().parent.parent / "web"

MAX_MESSAGE_CHARS = 500
MAX_HISTORY_PAIRS = 3
MAX_BODY_BYTES = 20_000

FALLBACK_REPLY = "Hmm, my brain lagged for a sec. Say that again?"

# Generate one reply at a time: on a CPU, running several generations
# in parallel only slows all of them down
model_lock = threading.Lock()


class ChatHandler(SimpleHTTPRequestHandler):

    # Windows can map .js to text/plain in the registry; be explicit
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".css": "text/css",
        ".html": "text/html",
        ".svg": "image/svg+xml",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_POST(self):

        if self.path != "/api/chat":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))

            if length <= 0 or length > MAX_BODY_BYTES:
                raise ValueError("bad length")

            body = json.loads(self.rfile.read(length))

            message = str(body.get("message", "")).strip()[:MAX_MESSAGE_CHARS]

            history = [
                (str(user)[:MAX_MESSAGE_CHARS], str(bot)[:MAX_MESSAGE_CHARS])
                for user, bot in list(body.get("history", []))[-MAX_HISTORY_PAIRS:]
            ]

        except (ValueError, TypeError, AttributeError):
            self.send_json({"error": "Invalid request"}, HTTPStatus.BAD_REQUEST)
            return

        if not message:
            self.send_json({"error": "Message is empty"}, HTTPStatus.BAD_REQUEST)
            return

        with model_lock:
            answer = respond(message, history)

        self.send_json({"reply": answer or FALLBACK_REPLY})

    def send_json(self, data, status=HTTPStatus.OK):

        payload = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)


def main():

    parser = argparse.ArgumentParser(description="ChatBot web server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--open", action="store_true", help="open the chat in your browser")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), ChatHandler)

    url = f"http://localhost:{args.port}"

    print(f"\nChatBot is running at {url}  (press Ctrl+C to stop)\n")

    if args.open:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
