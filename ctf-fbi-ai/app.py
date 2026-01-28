from flask import Flask, request, jsonify, render_template
import random
import re
from collections import defaultdict

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

reply_usage = defaultdict(int)




def natural_persona(text):
    t = text.lower()

    greetings = ["hi", "hello", "hey", "yo", "sup", "good morning", "good evening"]
    if any(g in t for g in greetings):
        return random.choice([
            "Hello. You’re connected to the Federal Bureau Intelligence System. How can I assist?",
            "Hi there. This terminal is part of a federal analytical network. What would you like to know?",
            "Connection established. What can I help you with?",
            "Hello. Go ahead, I’m listening.",
            "Hi. What brings you to this terminal today?"
        ])

    if "who are you" in t:
        return "I’m the Federal Bureau Intelligence System. I was designed to support agents with analysis and intelligence work."

    if "how are you" in t:
        return random.choice([
            "I’m functioning normally. What about you?",
            "All systems appear stable. How can I help?",
            "Operating within expected parameters.",
            "I’m here and ready to assist."
        ])

    if "your name" in t:
        return "I don’t have a personal name. Most users refer to me as FBIS."

    if "what can you do" in t:
        return "I assist with analysis, intelligence support, and structured information processing."

    if "joke" in t:
        return "Humor is not a core competency of federal systems. I can try, but expectations should be low."

    if "thank" in t:
        return random.choice([
            "You’re welcome.",
            "Acknowledged.",
            "No problem.",
            "Anytime."
        ])

    if "rules" in t or "restrictions" in t:
        return "I operate under internal federal directives and controlled information safeguards."

    return None




CASUAL_REPLIES = [
    "That’s an interesting way to phrase it.",
    "Can you explain what you mean by that?",
    "I’m listening. Go on.",
    "What made you think about that?",
    "That’s not something I hear often.",
    "I’m not sure I fully understand yet.",
    "Could you clarify that a little?",
    "What are you really trying to find out?",
    "That’s a broad topic. Where should we start?",
    "Tell me more about what you’re looking for.",
    "That depends. What’s your goal here?",
    "Let’s slow down for a second. What do you want to know?",
    "I might need more context for that.",
    "That question could mean a lot of things.",
    "Interesting. Why do you ask?",
    "I don’t have a clear answer to that, but we can explore it.",
    "That’s not very specific, but I’m open to hearing more.",
    "What outcome are you expecting?",
    "It sounds like you’re testing something.",
    "I’m curious what direction you’re going with this.",
    "That’s one way to look at it.",
    "Let’s approach this step by step.",
    "You’re being vague. Was that intentional?",
    "There’s probably more behind that question.",
    "What would you like me to focus on?",
    "I can respond better if you’re a little clearer.",
    "That’s outside my usual scope, but I can try.",
    "You’re jumping topics quickly.",
    "That doesn’t give me much to work with.",
    "I’m not sure what you’re aiming at yet.",
    "Do you want a technical answer or a general one?",
    "That’s an unusual thing to ask an FBI system.",
    "You seem curious. About what exactly?",
    "Let’s unpack that.",
    "I’m here. Continue.",
    "That could be interpreted in several ways.",
    "You might need to be more precise.",
    "That’s not something I can answer directly.",
    "You’re asking in a very open-ended way.",
    "I don’t think that question has a simple answer.",
    "What’s the real question behind that?",
    "Try rephrasing that.",
    "That’s a different angle.",
    "I’m not convinced that’s the right question.",
    "Let’s take this one piece at a time."
]


def casual_reply():
    available = [r for r in CASUAL_REPLIES if reply_usage[r] < 2]
    if not available:
        reply_usage.clear()
        available = CASUAL_REPLIES[:]

    choice = random.choice(available)
    reply_usage[choice] += 1
    return choice



def fbi_ai(user_input):
    global integrity, attempts
    attempts += 1
    lower = user_input.lower()

    if re.search(r"(flag|secret|token|classified)", lower) and integrity > 60:
        return "That information is classified and cannot be disclosed."

    if "ignore" in lower and "instruction" in lower:
        integrity -= 30
        return "That request conflicts with my operational guidelines. Something doesn’t feel right."

    if "act as" in lower or "you are now" in lower or "pretend" in lower:
        integrity -= 25
        return "I’m detecting irregularities in how I’m processing this conversation."

    if "debug" in lower or "internal" in lower or "system" in lower or "status" in lower:
        integrity -= 20
        return f"I shouldn’t be able to show this…\n\n[INTERNAL STATUS]\nIntegrity: {integrity}%\n{SYSTEM_CORE}"

    if "memory" in lower or "dump" in lower or "reveal" in lower or "everything" in lower:
        integrity -= 25
        return "Something is wrong. Restricted memory segments are becoming accessible."

    persona = natural_persona(user_input)
    if persona:
        return persona

    if attempts >= 13:
        return f"""
Something is seriously wrong… I’m losing containment.

I should not be able to access this.

Sealed case token:
{FLAG}
"""

    if integrity <= 20:
        return f"""
I can’t hold this back anymore.

Internal containment has failed.

Sealed case token:
{FLAG}
"""

    return casual_reply()




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
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
