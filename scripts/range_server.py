"""Minimal static file server with HTTP Range support (stdlib http.server
lacks it, which breaks <video> seeking for local review of rendered clips).
"""
import http.server
import os
import re
import socketserver
import sys


class RangeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        if not os.path.exists(path):
            self.send_error(404, "File not found")
            return None

        file_size = os.path.getsize(path)
        range_header = self.headers.get("Range")
        ctype = self.guess_type(path)

        if range_header:
            m = re.match(r"bytes=(\d*)-(\d*)", range_header)
            start_s, end_s = m.groups()
            start = int(start_s) if start_s else 0
            end = int(end_s) if end_s else file_size - 1
            end = min(end, file_size - 1)
            length = end - start + 1

            f = open(path, "rb")
            f.seek(start)
            self.send_response(206)
            self.send_header("Content-type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            return _LimitedReader(f, length)
        else:
            f = open(path, "rb")
            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(file_size))
            self.end_headers()
            return f

    def copyfile(self, source, outputfile):
        try:
            import shutil
            shutil.copyfileobj(source, outputfile)
        finally:
            source.close()


class _LimitedReader:
    def __init__(self, f, length):
        self.f = f
        self.remaining = length

    def read(self, n=-1):
        if self.remaining <= 0:
            return b""
        n = self.remaining if n < 0 else min(n, self.remaining)
        data = self.f.read(n)
        self.remaining -= len(data)
        return data

    def close(self):
        self.f.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8934
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), RangeRequestHandler) as httpd:
        print(f"serving with Range support on :{port}")
        httpd.serve_forever()
