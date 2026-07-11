#!/usr/bin/env python3
"""
serve.py — 캐시 비활성화 로컬 개발 서버
Cache-Control: no-store 헤더를 모든 응답에 추가합니다.
실기기(모바일) 확인 시 브라우저 캐시로 인한 오진을 방지합니다.

사용법:
  uv run python serve.py
  uv run python serve.py 9090  (포트 지정)
"""

import http.server
import sys


class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = http.server.HTTPServer(("", port), NoCacheHTTPRequestHandler)
    print(f"Serving on http://0.0.0.0:{port} (Cache-Control: no-store)")
    server.serve_forever()
