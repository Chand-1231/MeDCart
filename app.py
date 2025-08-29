import os
import sqlite3
from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = "replace_with_your_secret_key"

DB_PATH = os.path.join(os.path.dirname(__file__), "medcart.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

if not os.path.exists(DB_PATH):
    print("⚡ Creating medcart.db on first startup...")
    init_db()

@app.before_request
def ensure_cart_exists():
    if 'cart' not in session:
        session['cart'] = {}

def get_cart_count():
    return sum(session.get('cart', {}).values())

@app.route("/")
def home():
    return render_template("index.html", cart_count=get_cart_count())

@app.route("/shop")
def shop():
    products = [
        {"id": 1, "name": "Paracetamol", "price": "$5"},
        {"id": 2, "name": "Vitamin C", "price": "$10"}
    ]
    return render_template("shop.html", products=products, cart_count=get_cart_count())

@app.route("/cart")
def cart_view():
    return render_template("cart.html", cart_count=get_cart_count())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
