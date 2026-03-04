"""
captcha_demo.py — CAPTCHA + Turing Test Demo
AI Assignment 2 | Turing Test & CAPTCHA

Demonstrates both concepts side by side:
  1. CAPTCHA  — human vs bot detection
  2. Turing Test — can a machine imitate a human?

Run this file to see both in action.
"""

from captcha_generator import run_captcha_session, generate_captcha, validate_response


# ─── TURING TEST SIMULATION ───────────────────────────────────────────────────

# Predefined responses simulating a human participant
HUMAN_RESPONSES = {
    "what is your name":       "I'm Alex, nice to meet you!",
    "how are you":             "I'm doing well, thanks for asking.",
    "what is 2 + 2":           "That's 4, pretty easy!",
    "do you like music":       "Yes! I love listening to music when I study.",
    "are you a robot":         "No, I'm a real person talking to you.",
    "what is the weather like": "I haven't been outside yet today.",
    "tell me a joke":          "Why don't scientists trust atoms? Because they make up everything!",
}

# Predefined responses simulating an AI bot
BOT_RESPONSES = {
    "what is your name":       "I am an AI language model.",
    "how are you":             "I am functioning within normal parameters.",
    "what is 2 + 2":           "2 + 2 = 4.",
    "do you like music":       "I do not have preferences as I am an AI.",
    "are you a robot":         "I am an AI assistant designed to help you.",
    "what is the weather like": "I do not have access to real-time weather data.",
    "tell me a joke":          "Why did the computer go to the doctor? It had a virus.",
}


def get_response(response_map, question):
    """Match question to closest response in map."""
    question = question.lower().strip().rstrip("?")
    for key in response_map:
        if key in question or question in key:
            return response_map[key]
    return "I'm not sure how to answer that."


def run_turing_test():
    """
    Simplified Turing Test simulation.
    Judge asks questions to two participants (one human, one AI).
    Judge guesses which is human.
    """
    print("\n" + "=" * 55)
    print("  TURING TEST SIMULATION")
    print("=" * 55)
    print("  You are the judge. Ask questions to two participants.")
    print("  One is human, one is an AI bot.")
    print("  Try to figure out which is which!\n")

    # Randomly assign who is A and who is B
    import random
    if random.random() > 0.5:
        participant_a = ("HUMAN", HUMAN_RESPONSES)
        participant_b = ("BOT",   BOT_RESPONSES)
    else:
        participant_a = ("BOT",   BOT_RESPONSES)
        participant_b = ("HUMAN", HUMAN_RESPONSES)

    questions = [
        "what is your name",
        "how are you",
        "do you like music",
        "are you a robot",
        "tell me a joke",
    ]

    print("  Ask these questions to both participants:\n")
    for i, question in enumerate(questions, 1):
        print(f"  Q{i}: {question.capitalize()}?")
        print(f"  Participant A: {get_response(participant_a[1], question)}")
        print(f"  Participant B: {get_response(participant_b[1], question)}")
        print()

    print("-" * 55)
    guess = input("  Who is human — A or B? ").strip().upper()

    if guess == "A":
        actual = participant_a[0]
    elif guess == "B":
        actual = participant_b[0]
    else:
        print("  Invalid input.")
        return

    print()
    if actual == "HUMAN":
        print(f"  [✓] Correct! Participant {guess} was the HUMAN.")
        print("  The AI did not pass the Turing Test.")
    else:
        print(f"  [✗] Wrong! Participant {guess} was the BOT.")
        print("  The AI fooled you — it passed the Turing Test!")

    print(f"\n  Participant A was: {participant_a[0]}")
    print(f"  Participant B was: {participant_b[0]}")
    print("=" * 55)


# ─── MAIN DEMO ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  AI Assignment 2 — Turing Test & CAPTCHA Demo")
    print("=" * 55)
    print("\n  This demo shows two AI concepts:")
    print("  1. CAPTCHA  — prove you are human")
    print("  2. Turing Test — can AI imitate a human?\n")

    # Step 1 — CAPTCHA
    print("  STEP 1: Complete the CAPTCHA first.")
    verified = run_captcha_session()

    if verified:
        # Step 2 — Turing Test
        print("  STEP 2: Now try the Turing Test.")
        run_turing_test()
    else:
        print("  CAPTCHA failed. Cannot proceed to Turing Test.")
