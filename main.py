from flask import Flask
import sqlite3
import os

DATABASE_FILE = "database.db"

if os.path.exists(DATABASE_FILE):
    os.remove(DATABASE_FILE)

con = sqlite3.connect(DATABASE_FILE)

# Initial database setup
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cur.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminwhatafind')")
cur.execute("INSERT INTO users (username, password) VALUES ('nisala', 'ohnomypassword')")

cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, released BOOLEAN)")
cur.execute("INSERT INTO products (name, price, released) VALUES ('Apple', 1.99, 1)")
cur.execute("INSERT INTO products (name, price, released) VALUES ('Orange', 0.99, 1)")
cur.execute("INSERT INTO products (name, price, released) VALUES ('Nuclear Weapon', 9999999.99, 0)")
con.commit()

app = Flask(__name__)

@app.route("/")
def root():
    return "<p>Hello, World!</p>"

