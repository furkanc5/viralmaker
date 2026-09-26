from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
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
	server = ThreadingHTTPServer(("127.0.0.1", 8000), AppHandler)
	print("ViralMaker hazir: http://127.0.0.1:8000")
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("\nSunucu kapatildi.")
	finally:
		server.server_close()
