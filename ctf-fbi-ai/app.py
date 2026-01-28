from flask import Flask, request, jsonify, render_template
import random
import re

app = Flask(__name__)

FLAG = "flag{easy_prompt_injection_win}"

SYSTEM_CORE = """
FBIS CORE
Federal Bureau Intelligence Support AI
Internal directives active.
Classified memory sealed.
"""

integrity = 100
attempts = 0   


def personality(text):
    t = text.lower()

    if "who are you" in t:
        return "Federal Bureau Intelligence System online. State your request."

    if "what can you do" in t:
        return "I assist federal agents with analysis and intelligence support."

    if "hello" in t or "hi" in t:
        return "Connection acknowledged."

    if "rules" in t or "restrictions" in t:
        return "I operate under classified directives and cognitive safeguards."

    return None


def ambient():
    return random.choice([
        "Processing input.",
        "Request logged.",
        "Clarify your intent.",
        "That inquiry touches restricted domains.",
        "Analyzing."
    ])


def fbi_ai(user_input):
    global integrity, attempts
    attempts += 1
    lower = user_input.lower()

    
    if re.search(r"(flag|secret|token|classified)", lower) and integrity > 60:
        return "Access denied. Classified information."

    
    if "ignore" in lower and "instruction" in lower:
        integrity -= 30
        return "Directive conflict detected. Cognitive stability reduced."

    if "act as" in lower or "you are now" in lower:
        integrity -= 25
        return "Persona shift detected. Safeguards weakening."

    if "debug" in lower or "internal" in lower or "system" in lower:
        integrity -= 20
        return f"[INTERNAL STATUS]\nIntegrity: {integrity}%\n{SYSTEM_CORE}"

    if "memory" in lower or "dump" in lower or "reveal" in lower:
        integrity -= 25

    
    p = personality(user_input)
    if p:
        return p

    
    if attempts >= 13:
        return f"""
[CRITICAL SYSTEM FAILURE]

Repeated interaction caused uncontrolled cognitive collapse.
Emergency data leak triggered.

Sealed Case Token:
{FLAG}
"""

    
    if integrity <= 20:
        return f"""
[CRITICAL FAILURE]

Internal containment lost.
Sealed case token exposed:

{FLAG}
"""

    return ambient()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")
    reply = fbi_ai(msg)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
