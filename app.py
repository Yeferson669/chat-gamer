from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

messages = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/api/messages")
def get_messages():
    room = request.args.get("room")
    return jsonify(messages.get(room, []))


@app.post("/api/messages")
def send_message():
    data = request.json
    room = data["room"]

    msg = {
        "user": data["user"],
        "text": data["text"],
        "time": datetime.now().strftime("%H:%M")
    }

    messages.setdefault(room, []).append(msg)
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
