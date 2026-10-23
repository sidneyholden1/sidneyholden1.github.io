#!/usr/bin/env python3
"""Preview the public docs/ folder on loopback, including MP4 byte ranges."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = (Path(__file__).resolve().parents[1] / "docs").resolve()


class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def list_directory(self, path):
        self.send_error(404)
        return None

    def send_head(self):
        self.byte_range = None
        requested = unquote(urlsplit(self.path).path)
        if any(part.startswith(".") for part in Path(requested).parts[1:]):
            self.send_error(404)
            return None
        target = Path(self.translate_path(self.path)).resolve()
        if target != ROOT and ROOT not in target.parents:
            self.send_error(404)
            return None
        header = self.headers.get("Range")
        if not header or not target.is_file():
            return super().send_head()

        match = re.fullmatch(r"bytes=(\d*)-(\d*)", header.strip())
        size = target.stat().st_size
        if not match or not any(match.groups()) or size == 0:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        first, last = match.groups()
        if first:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1
        else:
            start = max(0, size - int(last))
            end = size - 1
        if start >= size or start > end:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None

        stream = target.open("rb")
        stream.seek(start)
        self.byte_range = (start, end)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(str(target)))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        return stream

    def copyfile(self, source, outputfile):
        try:
            if self.byte_range is None:
                return super().copyfile(source, outputfile)
            remaining = self.byte_range[1] - self.byte_range[0] + 1
            while remaining:
                chunk = source.read(min(65536, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8889)
    args = parser.parse_args()
    handler = partial(PreviewHandler, directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
        print(f"Local: http://127.0.0.1:{args.port}/", flush=True)
        print("Serving the website draft. Refresh after edits; Ctrl-C stops preview.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
