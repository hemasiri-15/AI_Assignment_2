"""
captcha_image.py — Image-based CAPTCHA Generator
AI Assignment 2 | Turing Test & CAPTCHA

Generates a real distorted CAPTCHA image using Pillow (PIL).
Saves the image as captcha_sample.png for demonstration.

Features:
- Random alphanumeric text
- Character rotation and spacing
- Noise lines across image
- Random dot noise
- Colour variation per character
"""

import random
import string
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ─── CONFIGURATION ────────────────────────────────────────────────────────────

WIDTH       = 200
HEIGHT      = 80
BG_COLOR    = (255, 255, 255)
TEXT_LENGTH = 6


# ─── CAPTCHA GENERATOR ───────────────────────────────────────────────────────

def generate_captcha_text(length=TEXT_LENGTH):
    """Generate random alphanumeric CAPTCHA string."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def get_font(size=36):
    """Load a font — falls back to default if no TTF available."""
    try:
        # Try common system fonts
        for font_path in [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        ]:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
    except Exception:
        pass
    return ImageFont.load_default()


def add_noise_lines(draw, width, height, count=6):
    """Add random lines across the image to confuse bots."""
    for _ in range(count):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        color = (
            random.randint(100, 200),
            random.randint(100, 200),
            random.randint(100, 200)
        )
        draw.line([(x1, y1), (x2, y2)], fill=color, width=1)


def add_noise_dots(draw, width, height, count=80):
    """Add random dots to make OCR harder."""
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        color = (
            random.randint(0, 200),
            random.randint(0, 200),
            random.randint(0, 200)
        )
        draw.point((x, y), fill=color)


def draw_characters(image, text, width, height):
    """
    Draw each character with random rotation and color.
    Each character is drawn on its own sub-image then pasted.
    """
    char_width = width // len(text)
    font = get_font(size=38)

    for i, char in enumerate(text):
        # Random color per character (dark colors for readability)
        color = (
            random.randint(0, 150),
            random.randint(0, 150),
            random.randint(0, 150)
        )

        # Create small image for this character
        char_img = Image.new("RGBA", (char_width, height), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((5, 10), char, font=font, fill=color)

        # Random rotation between -30 and +30 degrees
        angle = random.randint(-30, 30)
        char_img = char_img.rotate(angle, expand=False)

        # Paste onto main image with random vertical offset
        y_offset = random.randint(-5, 5)
        image.paste(char_img, (i * char_width, y_offset), char_img)

    return image


def generate_captcha_image(save_path="captcha_sample.png"):
    """
    Full CAPTCHA image generation pipeline:
    1. Generate random text
    2. Draw distorted characters
    3. Add noise lines and dots
    4. Apply slight blur
    5. Save image
    """
    captcha_text = generate_captcha_text()

    # Create base image
    image = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw  = ImageDraw.Draw(image)

    # Add noise first (behind text)
    add_noise_lines(draw, WIDTH, HEIGHT, count=6)
    add_noise_dots(draw, WIDTH, HEIGHT, count=80)

    # Draw characters with distortion
    image = draw_ch
