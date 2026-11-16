"""Deliver the committed artwork using only the Python standard library."""
import os
from pathlib import Path
import struct
import sys
import tempfile
import zlib


def validate_png(data):
    if not 0 < len(data) <= 1048576 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Artwork must be a PNG no larger than 1 MiB")
    offset = 8
    first = True
    saw_data = False
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError("Truncated PNG chunk")
        length = struct.unpack_from(">I", data, offset)[0]
        end = offset + length + 12
        if end > len(data):
            raise ValueError("Incomplete PNG payload")
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:end - 4]
        crc = struct.unpack_from(">I", data, end - 4)[0]
        if zlib.crc32(kind + payload) & 0xffffffff != crc:
            raise ValueError("PNG checksum mismatch")
        if first:
            if kind != b"IHDR" or length != 13:
                raise ValueError("Missing PNG header")
            width, height = struct.unpack_from(">II", payload)
            if not (1 <= width <= 1024 and 1 <= height <= 1024):
                raise ValueError("Artwork dimensions exceed competition limits")
            first = False
        saw_data |= kind == b"IDAT"
        if kind == b"IEND":
            if length or end != len(data) or not saw_data:
                raise ValueError("Invalid PNG ending")
            return
        offset = end
    raise ValueError("PNG has no end marker")


def main():
    source = Path(__file__).resolve().with_name("entry.png")
    data = source.read_bytes()
    validate_png(data)
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination, prefix=".entry-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
        os.replace(temporary, destination / "entry.png")
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Cannot deliver artwork: {error}", file=sys.stderr)
        sys.exit(1)
