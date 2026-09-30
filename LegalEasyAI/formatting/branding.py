from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


def ensure_logo_png(
    output_path: Path,
) -> Path:
    """
    Create a simple LegalEase PNG logo if one
    does not already exist.
    """

    output_path = Path(
        output_path
    )

    if output_path.exists():
        return output_path

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image = Image.new(
        "RGB",
        (512, 512),
        "white",
    )

    draw = ImageDraw.Draw(
        image
    )

    # Dark background.
    draw.rounded_rectangle(
        (20, 20, 492, 492),
        radius=85,
        fill="#0f172a",
    )

    # Document.
    draw.rounded_rectangle(
        (125, 85, 365, 425),
        radius=25,
        fill="#f8fafc",
    )

    # Document corner.
    draw.polygon(
        [
            (285, 85),
            (365, 165),
            (285, 165),
        ],
        fill="#60a5fa",
    )

    # Document lines.
    for y, width in [
        (205, 145),
        (250, 145),
        (295, 105),
        (340, 130),
    ]:

        draw.rounded_rectangle(
            (
                165,
                y,
                165 + width,
                y + 13,
            ),
            radius=6,
            fill="#0f172a",
        )

    # Small gold legal accent.
    draw.line(
        (350, 70, 430, 150),
        fill="#fbbf24",
        width=14,
    )

    draw.line(
        (390, 110, 345, 155),
        fill="#fbbf24",
        width=8,
    )

    image.save(
        output_path,
        format="PNG",
    )

    return output_path