from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance REAL,
            clicks INTEGER,
            cakes INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Server is running"

@app.route("/get_user", methods=["POST"])
def get_user():
    user_id = request.json["user_id"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()

    if not user:
        c.execute("INSERT INTO users VALUES (?, 0, 0, 0)", (user_id,))
        conn.commit()
        balance, clicks, cakes = 0, 0, 0
    else:
        balance, clicks, cakes = user[1], user[2], user[3]

    conn.close()

    return jsonify({
        "balance": balance,
        "clicks": clicks,
        "cakes": cakes
    })

@app.route("/save_user", methods=["POST"])
def save_user():
    data = request.json

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        UPDATE users
        SET balance=?, clicks=?, cakes=?
        WHERE user_id=?
    """, (data["balance"], data["clicks"], data["cakes"], data["user_id"]))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)