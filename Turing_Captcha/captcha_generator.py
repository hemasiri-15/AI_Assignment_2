"""
captcha_generator.py — CAPTCHA Generator
AI Assignment 2 | Turing Test & CAPTCHA

Generates a simple text-based CAPTCHA challenge and validates
the user's response. Demonstrates the core CAPTCHA concept:
distinguish human users from automated bots.

Architecture:
  Challenge Generator → User Interface → Response Validator → Allow/Deny

No external image libraries required — uses terminal-based distortion.
"""

import random
import string
import time


# ─── CHALLENGE GENERATOR ─────────────────────────────────────────────────────

def generate_captcha(length=6):
    """
    Generate a random CAPTCHA string.
    Mix of uppercase letters and digits — harder for bots to guess.
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def distort_captcha(text):
    """
    Visually distort the CAPTCHA text for terminal display.
    Simulates what image-based CAPTCHAs do visually.
    """
    noise_chars = ['*', '.', '~', '-', '^']
    distorted = ""
    for ch in text:
        noise = random.choice(noise_chars)
        side  = random.choice(['left', 'right', 'both', 'none'])
        if side == 'left':
            distorted += noise + ch + " "
        elif side == 'right':
            distorted += ch + noise + " "
        elif side == 'both':
            distorted += noise + ch + noise + " "
        else:
            distorted += ch + "  "
    return distorted.strip()


# ─── BOT DETECTION LOGIC ─────────────────────────────────────────────────────

def is_too_fast(elapsed_seconds, threshold=1.5):
    """
    Bots typically respond in milliseconds.
    Humans take at least 1-2 seconds to read and type.
    Returns True if response was suspiciously fast (likely a bot).
    """
    return elapsed_seconds < threshold


# ─── RESPONSE VALIDATOR ──────────────────────────────────────────────────────

def validate_response(correct, user_input):
    """
    Compare user input with correct CAPTCHA (case-insensitive).
    """
    return user_input.strip().upper() == correct.upper()


# ─── CAPTCHA SESSION ─────────────────────────────────────────────────────────

def run_captcha_session(max_attempts=3):
    """
    Full CAPTCHA session:
      1. Generate challenge
      2. Display to user
      3. Record response + timing
      4. Validate
      5. Allow or deny

    Returns True if human verified, False if denied.
    """
    captcha_text = generate_captcha()

    print("\n" + "=" * 50)
    print("  CAPTCHA VERIFICATION")
    print("=" * 50)
    print("  Prove you are human.")
    print("  Type the characters you see below:\n")
    print(f"    {distort_captcha(captcha_text)}")
    print()

    for attempt in range(1, max_attempts + 1):
        start_time = time.time()
        user_input  = input(f"  Enter CAPTCHA (attempt {attempt}/{max_attempts}): ")
        elapsed     = time.time() - start_time

        # Bot detection — response too fast
        if is_too_fast(elapsed):
            print(f"  [WARNING] Response in {elapsed:.2f}s — suspiciously fast.")
            print("  [BOT DETECTED] Access denied.\n")
            return False

        # Validate response
        if validate_response(captcha_text, user_input):
            print(f"  [✓] Correct! Verified as human in {elapsed:.1f}s.")
            print("  [ACCESS GRANTED]\n")
            return True
        else:
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"  [✗] Incorrect. {remaining} attempt(s) remaining.\n")
                print(f"    {distort_captcha(captcha_text)}\n")
            else:
                print("  [✗] Too many failed attempts.")
                print("  [ACCESS DENIED]\n")

    return False


if __name__ == "__main__":
    result = run_captcha_session()
    if not result:
        print("  Verification failed. Please try again later.")
