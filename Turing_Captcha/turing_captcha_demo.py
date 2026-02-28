"""
Turing Test and CAPTCHA Demo
Reference: AIMA Chapter 1
"""

import random
import string
import time


class TuringTestBot:
    def __init__(self):
        self.rules = [
            (["hello", "hi", "hey"],
             ["Hey! How are you?", "Hi there!", "Hello!"]),
            (["how are you"],
             ["I am good thanks!", "Pretty well actually.", "Fine, and you?"]),
            (["your name", "who are you"],
             ["You can call me Alex.", "I am just someone online.", "Does it matter?"]),
            (["weather"],
             ["Quite cloudy here.", "Hot today!", "A bit chilly."]),
            (["ai", "robot", "bot", "machine"],
             ["Ha, I am not a robot!", "Why would I be a bot?", "Definitely human."]),
            (["bye", "goodbye"],
             ["Take care!", "Bye!", "See you later!"]),
        ]
        self.defaults = [
            "Interesting, tell me more.",
            "I am not sure about that.",
            "That is a good point.",
            "Yeah I get what you mean.",
            "Can you explain more?",
        ]

    def respond(self, user_input):
        text = user_input.lower()
        for (keywords, responses) in self.rules:
            if any(kw in text for kw in keywords):
                time.sleep(random.uniform(0.3, 0.8))
                return random.choice(responses)
        time.sleep(random.uniform(0.4, 1.0))
        return random.choice(self.defaults)


class TextCAPTCHA:
    def __init__(self, length=6, max_attempts=3, timeout=60):
        self.length       = length
        self.max_attempts = max_attempts
        self.timeout      = timeout
        self._answer      = None
        self._start       = None

    def generate(self):
        chars = string.ascii_uppercase + string.digits
        for ch in ["0", "O", "1", "I", "L"]:
            chars = chars.replace(ch, "")
        self._answer = "".join(random.choices(chars, k=self.length))
        self._start  = time.time()
        return self._answer

    def display(self, text):
        noise = r"/\|-+.*"
        top   = "".join(random.choices(noise, k=26))
        bot   = "".join(random.choices(noise, k=26))
        sp    = "  ".join(list(text))
        print()
        print("  +----------------------------+")
        print("  |  " + top + "  |")
        print("  |                            |")
        print("  |    " + sp + "    |")
        print("  |                            |")
        print("  |  " + bot + "  |")
        print("  +----------------------------+")
        print("  Type the characters above (not case sensitive)")
        print()

    def verify(self, response):
        if self._answer is None:
            return False, "No challenge generated."
        elapsed = time.time() - self._start
        if elapsed < 1.0:
            return False, "Too fast. Possible bot."
        if elapsed > self.timeout:
            return False, "Timed out."
        if response.upper().strip() == self._answer:
            return True, "CAPTCHA passed in {:.1f} seconds.".format(elapsed)
        return False, "Wrong. Expected {} got {}.".format(
            self._answer, response.upper().strip()
        )


def run_turing():
    print()
    print("=" * 50)
    print("  TURING TEST DEMO")
    print("  Can you tell this is a machine?")
    print("  Type quit to exit")
    print("=" * 50)
    bot = TuringTestBot()
    while True:
        try:
            msg = input("  You : ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not msg:
            continue
        if msg.lower() in ["quit", "exit"]:
            print("  Bot :", bot.respond("bye"))
            break
        print("  Bot :", bot.respond(msg))
        print()


def run_captcha():
    print()
    print("=" * 50)
    print("  CAPTCHA DEMO")
    print("=" * 50)
    c      = TextCAPTCHA()
    passed = False
    for attempt in range(1, c.max_attempts + 1):
        print("  Attempt {} of {}".format(attempt, c.max_attempts))
        challenge = c.generate()
        c.display(challenge)
        try:
            ans = input("  Your answer: ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        ok, msg = c.verify(ans)
        print("  Result:", msg)
        if ok:
            passed = True
            break
        if attempt < c.max_attempts:
            print("  New challenge coming...")
    print()
    if passed:
        print("  ACCESS GRANTED")
    else:
        print("  ACCESS DENIED")
    print()


if __name__ == "__main__":
    print()
    print("=" * 50)
    print("  TURING TEST AND CAPTCHA")
    print("=" * 50)
    print("  1. Turing Test Bot")
    print("  2. CAPTCHA")
    print("  3. Exit")
    print()
    while True:
        try:
            ch = input("  Choice (1/2/3): ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if ch == "1":
            run_turing()
        elif ch == "2":
            run_captcha()
        elif ch == "3":
            print("  Goodbye!")
            break
        else:
            print("  Enter 1, 2, or 3")
