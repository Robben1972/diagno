import qrcode
from io import BytesIO

def generate_qr_png_bytes(link: str) -> bytes:
    img = qrcode.make(link)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
