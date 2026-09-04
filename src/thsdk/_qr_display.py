from __future__ import annotations

import os
import struct
import sys
import urllib.request
import zlib
from threading import Thread
from typing import Any, TextIO
from urllib.parse import urlsplit


_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_MAX_IMAGE_BYTES = 2 * 1024 * 1024
_MAX_IMAGE_SIDE = 1024
_MAX_RENDER_SECONDS = 5.0
_QUIET_ZONE = 4


def print_qr_challenge(
    challenge: dict[str, Any],
    *,
    stream: TextIO | None = None,
    render_timeout: float = _MAX_RENDER_SECONDS,
) -> None:
    """Best-effort display of one QR challenge; output never controls authentication."""
    output = stream or sys.stdout
    image_url = str(challenge.get("image_url") or "").strip()
    scan_url = str(challenge.get("scan_url") or "").strip()

    _write_line(
        output,
        "请使用同花顺手机客户端扫码确认登录：",
        "Scan with the mobile app to confirm login:",
    )
    _flush(output)

    rendered = False
    if image_url and render_timeout > 0:
        try:
            modules = _load_qr_modules(
                image_url,
                timeout=min(float(render_timeout), _MAX_RENDER_SECONDS),
            )
            if modules is not None:
                rendered = _write_terminal_qr(modules, output)
        except Exception:
            rendered = False
    if rendered:
        if scan_url:
            _write_line(output, f"扫码地址：{scan_url}", f"Scan URL: {scan_url}")
        elif image_url:
            _write_line(output, f"二维码图片：{image_url}", f"QR image: {image_url}")
    elif image_url:
        _write_line(
            output,
            "当前终端未能显示二维码，请打开二维码图片地址。",
            "The QR code could not be rendered; open the QR image URL instead.",
        )
        _write_line(output, f"二维码图片：{image_url}", f"QR image: {image_url}")
    elif scan_url:
        _write_line(output, f"扫码地址：{scan_url}", f"Scan URL: {scan_url}")
    _flush(output)


def _write_line(stream: TextIO, value: str, ascii_fallback: str) -> bool:
    try:
        print(value, file=stream)
        return True
    except UnicodeError:
        try:
            print(ascii_fallback, file=stream)
            return True
        except Exception:
            return False
    except Exception:
        return False


def _flush(stream: TextIO) -> None:
    try:
        stream.flush()
    except Exception:
        pass


def _load_qr_modules(url: str, *, timeout: float) -> list[list[bool]] | None:
    """Bound image work even when a server keeps a socket alive indefinitely."""
    if timeout <= 0:
        return None

    result: list[list[list[bool]]] = []

    def load() -> None:
        try:
            result.append(_qr_modules(_download_png(url)))
        except Exception:
            pass

    worker = Thread(target=load, name="thsdk-qr-display", daemon=True)
    worker.start()
    worker.join(timeout)
    return result[0] if result else None


def _download_png(url: str) -> bytes:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("二维码图片地址必须使用 HTTPS")
    request = urllib.request.Request(url, headers={"User-Agent": "THSDK/2 QR Login"})
    with urllib.request.urlopen(request, timeout=5) as response:
        final_url = urlsplit(response.geturl())
        if final_url.scheme != "https":
            raise ValueError("二维码图片重定向必须使用 HTTPS")
        data = response.read(_MAX_IMAGE_BYTES + 1)
    if len(data) > _MAX_IMAGE_BYTES:
        raise ValueError("二维码图片过大")
    return data


def _qr_modules(data: bytes) -> list[list[bool]]:
    pixels = _decode_png(data)
    left = len(pixels[0])
    top = len(pixels)
    right = -1
    bottom = -1
    for y, row in enumerate(pixels):
        for x, is_black in enumerate(row):
            if not is_black:
                continue
            left = min(left, x)
            top = min(top, y)
            right = max(right, x)
            bottom = max(bottom, y)

    if right < 0:
        raise ValueError("二维码图片没有有效图案")
    width = right - left + 1
    height = bottom - top + 1

    candidates: list[tuple[float, int, list[list[bool]]]] = []
    image_height = len(pixels)
    image_width = len(pixels[0])
    for size in range(21, 178, 4):
        scale_x = width / size
        scale_y = height / size
        scale = round((scale_x + scale_y) / 2)
        if scale < 1 or abs(scale_x - scale) > 0.08 or abs(scale_y - scale) > 0.08:
            continue
        if left + size * scale > image_width or top + size * scale > image_height:
            continue
        matrix = _sample_modules(pixels, left, top, size, scale)
        score = _finder_score(matrix)
        candidates.append((score, scale, matrix))

    if not candidates:
        raise ValueError("无法识别二维码模块")
    score, _, matrix = max(candidates, key=lambda item: (item[0], item[1]))
    if score < 0.85:
        raise ValueError("二维码定位图案无效")
    return matrix


def _decode_png(data: bytes) -> list[list[bool]]:
    if not data.startswith(_PNG_SIGNATURE):
        raise ValueError("二维码图片不是 PNG")

    ihdr: bytes | None = None
    idat: list[bytes] = []
    position = len(_PNG_SIGNATURE)
    while position + 12 <= len(data):
        length = struct.unpack(">I", data[position : position + 4])[0]
        kind = data[position + 4 : position + 8]
        end = position + 12 + length
        if end > len(data):
            raise ValueError("PNG 数据不完整")
        payload = data[position + 8 : position + 8 + length]
        if kind == b"IHDR":
            ihdr = payload
        elif kind == b"IDAT":
            idat.append(payload)
        elif kind == b"IEND":
            break
        position = end

    if ihdr is None or len(ihdr) != 13 or not idat:
        raise ValueError("PNG 缺少必要数据")
    width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(
        ">IIBBBBB", ihdr
    )
    channels = {0: 1, 2: 3, 4: 2, 6: 4}.get(color_type)
    if (
        channels is None
        or bit_depth != 8
        or compression != 0
        or filter_method != 0
        or interlace != 0
        or not 1 <= width <= _MAX_IMAGE_SIDE
        or not 1 <= height <= _MAX_IMAGE_SIDE
    ):
        raise ValueError("PNG 格式不受支持")

    stride = width * channels
    expected_size = (stride + 1) * height
    decompressor = zlib.decompressobj()
    raw = decompressor.decompress(b"".join(idat), expected_size + 1)
    if len(raw) != expected_size or decompressor.unconsumed_tail or not decompressor.eof:
        raise ValueError("PNG 像素数据无效")

    rows: list[list[bool]] = []
    previous = bytearray(stride)
    offset = 0
    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        current = bytearray(raw[offset : offset + stride])
        offset += stride
        if filter_type not in {0, 1, 2, 3, 4}:
            raise ValueError("PNG 滤镜不受支持")
        for index, value in enumerate(current):
            left = current[index - channels] if index >= channels else 0
            above = previous[index]
            upper_left = previous[index - channels] if index >= channels else 0
            if filter_type == 1:
                current[index] = (value + left) & 0xFF
            elif filter_type == 2:
                current[index] = (value + above) & 0xFF
            elif filter_type == 3:
                current[index] = (value + ((left + above) // 2)) & 0xFF
            elif filter_type == 4:
                current[index] = (value + _paeth(left, above, upper_left)) & 0xFF

        row: list[bool] = []
        for index in range(0, stride, channels):
            if color_type in {0, 4}:
                red = green = blue = current[index]
            else:
                red, green, blue = current[index : index + 3]
            alpha = current[index + channels - 1] if color_type in {4, 6} else 255
            luminance = (299 * red + 587 * green + 114 * blue) // 1000
            luminance = (luminance * alpha + 255 * (255 - alpha)) // 255
            row.append(luminance < 128)
        rows.append(row)
        previous = current
    return rows


def _paeth(left: int, above: int, upper_left: int) -> int:
    prediction = left + above - upper_left
    left_distance = abs(prediction - left)
    above_distance = abs(prediction - above)
    upper_left_distance = abs(prediction - upper_left)
    if left_distance <= above_distance and left_distance <= upper_left_distance:
        return left
    if above_distance <= upper_left_distance:
        return above
    return upper_left


def _sample_modules(
    pixels: list[list[bool]], left: int, top: int, size: int, scale: int
) -> list[list[bool]]:
    matrix: list[list[bool]] = []
    threshold = scale * scale / 2
    for module_y in range(size):
        row: list[bool] = []
        start_y = top + module_y * scale
        for module_x in range(size):
            start_x = left + module_x * scale
            black = sum(
                pixels[y][x]
                for y in range(start_y, start_y + scale)
                for x in range(start_x, start_x + scale)
            )
            row.append(black >= threshold)
        matrix.append(row)
    return matrix


def _finder_score(matrix: list[list[bool]]) -> float:
    size = len(matrix)
    matches = 0
    total = 0
    for origin_x, origin_y in ((0, 0), (size - 7, 0), (0, size - 7)):
        for y in range(7):
            for x in range(7):
                edge = x in {0, 6} or y in {0, 6}
                center = 2 <= x <= 4 and 2 <= y <= 4
                expected = edge or center
                matches += matrix[origin_y + y][origin_x + x] == expected
                total += 1
    return matches / total


def _write_terminal_qr(matrix: list[list[bool]], stream: TextIO) -> bool:
    encoding = getattr(stream, "encoding", None) or "utf-8"
    try:
        "█▀▄".encode(encoding)
    except (LookupError, UnicodeEncodeError):
        return False

    size = len(matrix)
    white_row = [False] * (size + _QUIET_ZONE * 2)
    padded = [white_row[:] for _ in range(_QUIET_ZONE)]
    padded.extend(
        [[False] * _QUIET_ZONE + row + [False] * _QUIET_ZONE for row in matrix]
    )
    padded.extend([white_row[:] for _ in range(_QUIET_ZONE)])
    if len(padded) % 2:
        padded.append(white_row[:])

    ansi = (
        bool(getattr(stream, "isatty", lambda: False)())
        and os.getenv("TERM", "") != "dumb"
    )
    symbols = {
        (False, False): " ",
        (True, True): "█",
        (True, False): "▀",
        (False, True): "▄",
    }
    stream.write("\n")
    for index in range(0, len(padded), 2):
        pairs = zip(padded[index], padded[index + 1])
        line = "".join(symbols[(top, bottom)] for top, bottom in pairs)
        if ansi:
            stream.write(f"\x1b[30;47m{line}\x1b[0m\n")
        else:
            stream.write(f"{line}\n")
    return True


__all__: list[str] = []
