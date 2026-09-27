from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class AppHandler(SimpleHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, directory=str(ROOT), **kwargs)

	def do_GET(self):
		if self.path in ("/", "/index.html"):
			self.path = "/index.html"
		return super().do_GET()


if __name__ == "__main__":
	host = "0.0.0.0"
	port = int(os.environ.get("PORT", "8000"))
	server = ThreadingHTTPServer((host, port), AppHandler)
	print(f"ViralMaker hazir: http://{host}:{port}")
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("\nSunucu kapatildi.")
	finally:
		server.server_close()
