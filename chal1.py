from flask import Flask, render_template, render_template_string, request
import sqlite3
import os
import json
import base64

DATABASE_FILE = "database.db"

if os.path.exists(DATABASE_FILE):
    os.remove(DATABASE_FILE)

with sqlite3.connect(DATABASE_FILE) as conn:
    # Initial database setup
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, active BOOLEAN)")
    cur.execute("INSERT INTO users (username, password, active) VALUES ('admin', 'adminwhatafind', 1)")
    cur.execute("INSERT INTO users (username, password, active) VALUES ('nisala', 'ohnomypassword', 1)")

    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, released BOOLEAN)")
    cur.execute("INSERT INTO products (name, price, released) VALUES ('Apple', 1.99, 1)")
    cur.execute("INSERT INTO products (name, price, released) VALUES ('Orange', 0.99, 1)")
    cur.execute("INSERT INTO products (name, price, released) VALUES ('Nuclear Weapon', 9999999.99, 0)")
    conn.commit()

app = Flask(__name__)

app.secret_key = "wowmysupersecretkeythatiwilluseforencryptingeverything"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    name = request.args.get("name")
    name = base64.b64decode(name).decode("utf-8")
    # couldn't figure out how to pass args to render_template
    file_data = open("templates/products.html", "r").read()
    file_data = file_data.replace("{{name}}", name)
    return render_template_string(file_data)

@app.route("/api/products", methods=["POST"])
def products_api():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cur = conn.cursor()
        sfilter = request.form["filter"]
        if sfilter is None:
            sfilter = ""

        cur.execute(f"SELECT * FROM products WHERE released = 1 AND name LIKE '%{sfilter}%'")
        products = cur.fetchall()
        return json.dumps(products)
