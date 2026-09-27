from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from email.parser import BytesParser
from email.policy import default
import os
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent


class AppHandler(SimpleHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, directory=str(ROOT), **kwargs)

	def do_GET(self):
		path = urlsplit(self.path).path
		if path in ("/", "/index.html"):
			self.path = "/index.html"
		elif path == "/background-remover":
			self.path = "/background-remover.html"
		return super().do_GET()

	def do_OPTIONS(self):
		if urlsplit(self.path).path == "/api/remove-background":
			self.send_response(204)
			self.send_cors_headers()
			self.end_headers()
			return
		self.send_error(404, "Endpoint bulunamadi")

	def send_cors_headers(self):
		self.send_header("Access-Control-Allow-Origin", os.environ.get("FRONTEND_ORIGIN", "*"))
		self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
		self.send_header("Access-Control-Allow-Headers", "Content-Type")

	def do_POST(self):
		if urlsplit(self.path).path != "/api/remove-background":
			self.send_error(404, "Endpoint bulunamadi")
			return

		try:
			content_length = int(self.headers.get("Content-Length", "0"))
		except ValueError:
			self.send_error(400, "Gecersiz dosya boyutu")
			return

		if content_length <= 0 or content_length > 15 * 1024 * 1024:
			self.send_error(413, "Dosya 15 MB'dan kucuk olmali")
			return

		content_type = self.headers.get("Content-Type", "")
		if not content_type.startswith("multipart/form-data"):
			self.send_error(400, "multipart/form-data bekleniyor")
			return

		try:
			body = self.rfile.read(content_length)
			message = BytesParser(policy=default).parsebytes(
				f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode() + body
			)
			upload = next(
				(
					part
					for part in message.walk()
					if part.get_content_disposition() in ("form-data", "attachment")
					and part.get_param("name", header="content-disposition") == "image"
				),
				None,
			)
			image_data = upload.get_payload(decode=True) if upload else None
			if not image_data:
				self.send_error(400, "Gorsel bulunamadi")
				return

			from backgroundremover.bg import remove

			result = remove(
				image_data,
				model_name=os.environ.get("BACKGROUND_MODEL", "u2net"),
				alpha_matting=True,
				alpha_matting_foreground_threshold=240,
				alpha_matting_background_threshold=10,
				alpha_matting_erode_structure_size=10,
				alpha_matting_base_size=1000,
			)
			self.send_response(200)
			self.send_header("Content-Type", "image/png")
			self.send_header("Content-Length", str(len(result)))
			self.send_header("Cache-Control", "no-store")
			self.send_cors_headers()
			self.end_headers()
			self.wfile.write(result)
		except ModuleNotFoundError:
			self.send_error(503, "backgroundremover kurulu degil")
		except Exception as error:
			print(f"Arka plan silme hatasi: {error}")
			self.send_error(500, "Gorsel islenemedi")


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
