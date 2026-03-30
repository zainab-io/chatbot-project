from flask import Flask, render_template, request, jsonify, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# Country capitals database
capitals = {
    "bangladesh": "Dhaka 🇧🇩",
    "uae": "Abu Dhabi 🇦🇪",
    "india": "New Delhi 🇮🇳",
    "uk": "London 🇬🇧",
    "usa": "Washington, D.C. 🇺🇸",
    "france": "Paris 🇫🇷",
    "germany": "Berlin 🇩🇪"
}

def get_bot_response(user_input):
    user_input = user_input.lower()

    # Save history
    if "history" not in session:
        session["history"] = []

    session["history"].append(user_input)

    # Greeting
    if any(word in user_input for word in ["hi", "hello", "hey"]):
        return random.choice(["Hello! 👋", "Hi there! 😊", "Hey! How can I help?"])

    # Time & Date
    if "time" in user_input:
        return "Current time is " + datetime.now().strftime("%H:%M:%S")

    if "date" in user_input:
        return "Today's date is " + datetime.now().strftime("%d-%m-%Y")

    # Capital detection (ANY country in dictionary)
    if "capital" in user_input:
        for country in capitals:
            if country in user_input:
                return f"The capital of {country.title()} is {capitals[country]}"
        return "I don't have that country in my database yet 🌍"

    # Math
    if "calculate" in user_input:
        try:
            expression = user_input.replace("calculate", "")
            result = eval(expression)
            return f"Answer: {result}"
        except:
            return "Invalid calculation 😅"

    # Memory
    if "what did i say" in user_input:
        return "You said: " + ", ".join(session["history"][-3:])

    # AI explanation
    if "ai" in user_input:
        return "AI allows machines to learn, think, and make decisions 🤖"

    # Default
    return random.choice([
        "Interesting 🤔 tell me more!",
        "I'm still learning 😅",
        "Can you rephrase that?"
    ])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["msg"]
    response = get_bot_response(user_input)
    return jsonify({"response": response})

#if __name__ == "__main__":
    #app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)