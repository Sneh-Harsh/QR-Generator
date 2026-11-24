#!/usr/bin/env python3
"""Generate a PNG QR code from a link."""

import argparse
from pathlib import Path

try:
    import qrcode
except ImportError as exc:
    raise SystemExit(
        "The 'qrcode' package is required. Install dependencies with "
        "'python -m pip install -r requirements.txt'."
    ) from exc


def generate_qr(link: str, output: Path) -> None:
    """Create a QR code PNG containing link."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a QR code for a link.")
    parser.add_argument(
        "link",
        nargs="?",
        help="link to encode (if omitted, you'll be prompted)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("qr_code.png"),
        help="output image path (default: qr_code.png)",
    )
    args = parser.parse_args()

    link = args.link or input("Enter a link: ").strip()
    if not link:
        parser.error("a link is required")

    try:
        generate_qr(link, args.output)
    except OSError as exc:
        parser.error(f"could not save QR code to {args.output}: {exc}")

    print(f"QR code saved to {args.output}")


if __name__ == "__main__":
    main()
