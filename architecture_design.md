nano Turing_Captcha/architecture_design.md
```

Paste this:
```
# Turing Test and CAPTCHA — Architecture Design

Reference: AIMA Chapter 1

---

## 1. THE TURING TEST

Definition:
  Proposed by Alan Turing (1950).
  A human evaluator chats with a human and a machine (text only).
  If the evaluator cannot tell which is which, the machine passes.

Capabilities needed:
  - Natural Language Processing
  - Knowledge Representation
  - Automated Reasoning
  - Machine Learning

Architecture:

  +--------------------------------------------------+
  |              TURING TEST SYSTEM                  |
  +-------------------+------------------------------+
  |   HUMAN SIDE      |      MACHINE SIDE            |
  |                   |                              |
  |  Human types      |  NLP Engine                  |
  |  a message        |    |                         |
  |       |           |  Dialogue Manager            |
  |       |           |    |                         |
  |       |           |  Knowledge Base              |
  |       |           |    |                         |
  |       |           |  Response Generator          |
  +-------------------+------------------------------+
          |                   |
          +--------+----------+
                   |
            HUMAN EVALUATOR
          Human or Machine?

---

## 2. CAPTCHA

Definition:
  Completely Automated Public Turing test to tell Computers and Humans Apart.
  Exploits tasks easy for humans but hard for machines.

Architecture:

  STEP 1 — CHALLENGE GENERATOR
    Generate random string or images
    Apply distortion and noise
    Store correct answer

  STEP 2 — USER INTERFACE
    Display challenge to user
    Accept typed or click response

  STEP 3 — VERIFIER
    Compare response to stored answer
    Check timing (too fast = bot)
    Check mouse movement

    Result:
      PASS -> Grant Access
      FAIL -> New Challenge

Types of CAPTCHA:
  Text CAPTCHA    : distorted characters to type
  Image CAPTCHA   : select all traffic lights
  Audio CAPTCHA   : spoken digits with noise
  reCAPTCHA v3    : invisible behavioural scoring

---

## 3. COMPARISON

Feature       | Turing Test             | CAPTCHA
--------------|-------------------------|----------------
Purpose       | Evaluate AI intelligence| Block bots
Judge         | Human evaluator         | Automated verifier
Direction     | Machine pretends human  | Identify if user is human
Used in       | Research                | Every website

---

## 4. AGENT CLASSIFICATION

Turing Test Bot      : Learning Agent
CAPTCHA Generator    : Simple Reflex Agent
CAPTCHA Solver (bot) : Model-Based and Learning Agent

Reference: Russell and Norvig, AIMA 4th Edition, Chapter 1
