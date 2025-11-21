from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Usar la variable de entorno DATABASE_URL de Render
# Si quieres probar localmente, puedes reemplazar por tu URL externa directamente
DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql://chat_gamer_user:0GKauaXj0GE6nHngYDB1vAWZ2BRgFVSK@dpg-d4fudu0gjchc73dlll30-a.oregon-postgres.render.com/chat_gamer"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de mensajes
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(50))
    user = db.Column(db.String(50))
    text = db.Column(db.Text)
    time = db.Column(db.String(10))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/api/messages")
def get_messages():
    room = request.args.get("room")
    msgs = Message.query.filter_by(room=room).all()
    return jsonify([{"user": m.user, "text": m.text, "time": m.time} for m in msgs])

@app.post("/api/messages")
def send_message():
    data = request.json
    msg = Message(
        room=data["room"],
        user=data["user"],
        text=data["text"],
        time=datetime.now().strftime("%H:%M")
    )
    db.session.add(msg)
    db.session.commit()
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
