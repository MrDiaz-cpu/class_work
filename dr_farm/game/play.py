"""Start the local game with python play.py. Keep the forwarded port Private."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

import farm
from levels import FILES, FIELDS, layout

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
ASSETS = {"": ("index.html", "text/html"), "style.css": ("style.css", "text/css"),
          "app.js": ("app.js", "text/javascript"), "scene.js": ("scene.js", "text/javascript"),
          "sprites.js": ("sprites.js", "text/javascript")}


def simulate(level, field):
    try:
        process = subprocess.run([sys.executable, "-B", str(ROOT / "runner.py"), str(level), field],
                                 cwd=ROOT, capture_output=True, text=True,
                                 timeout=5, stdin=subprocess.DEVNULL)
        return json.loads(process.stdout)
    except subprocess.TimeoutExpired:
        return {"error": {"message": "Your code took too long. Is a loop stuck?"}}
    except (UnicodeError, ValueError):
        return {"error": {"message": "Python stopped before the farm was ready. Check your saved file."}}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, obj, mime="application/json", status=200):
        body = json.dumps(obj).encode() if mime == "application/json" else obj
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path[1:]
        if path == "api/levels":
            previews = {}
            for level, filename in enumerate(FILES):
                for name in FIELDS[level]:
                    setting = layout(level, name)
                    previews[f"{level}/{name}"] = dict(
                        state=farm.Farm(level, setting).state(), target=setting["target"],
                        filename=filename, best=setting["best"])
            return self.send(dict(fields=previews, grow=farm._GROW, sprites=sorted(
                p.stem for p in (WEB / "sprites").glob("*.png"))))
        if path in ASSETS:
            filename, mime = ASSETS[path]
            return self.send((WEB / filename).read_bytes(), mime + "; charset=utf-8")
        if re.fullmatch(r"sprites/[a-z0-9_]+\.png", path) and (WEB / path).is_file():
            return self.send((WEB / path).read_bytes(), "image/png")
        self.send({"error": "File not found."}, status=404)

    def do_POST(self):
        if urlsplit(self.path).path != "/api/run":
            return self.send({"error": "File not found."}, status=404)
        origin = self.headers.get("Origin")
        forwarded = self.headers.get("X-Forwarded-Host", "").split(",")[0].strip()
        if origin and urlsplit(origin).netloc not in {self.headers.get("Host"), forwarded}:
            return self.send({"error": "Open the game in its own forwarded tab."}, status=403)
        try:
            length = int(self.headers.get("Content-Length", 0))
            if not 0 < length < 512:
                raise ValueError
            body = json.loads(self.rfile.read(length))
            level, name = body["level"], body["field"]
            if type(level) is not int:
                raise ValueError
            layout(level, name)
        except (KeyError, ValueError, TypeError):
            return self.send({"error": "Pick a level and a field."}, status=400)
        self.send(simulate(level, name))


def main():
    parser = argparse.ArgumentParser(description="Play Dr. Farm with your saved Python.")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    try:
        server = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    except OSError:
        sys.exit(f"Port {args.port} is busy. Stop the other server or use --port {args.port + 1}.")
    print(f"Dr. Farm is running at http://localhost:{args.port}", flush=True)
    print(f"In cs50.dev, choose Ports → {args.port} → Open in Browser. Keep the port Private.")
    print("Save your file and click Run saved Python. Press Ctrl+C here to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

