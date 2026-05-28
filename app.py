from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import mysql.connector

app = Flask(__name__)
DB = "todo.db"


def db_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def log_query(sql):
    try:
        conn = mysql.connector.connect(
            host="MYSQL_IP",
            user="admin",
            password="1234",
            database="logdb"
        )

        cur = conn.cursor()
        qtype = sql.split()[0].lower()

        cur.execute(
            "INSERT INTO query_log (type, sql_text, datetime) VALUES (%s, %s, %s)",
            (qtype, sql, datetime.now())
        )

        conn.commit()
        conn.close()

    except Exception as e:
        print(e)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/todos", methods=["GET"])
def get_todos():
    conn = db_conn()
    cur = conn.cursor()
    sql = "SELECT * FROM todolist"
    cur.execute(sql)
    rows = cur.fetchall()
    log_query(sql)
    return jsonify([dict(r) for r in rows])


@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    sql = "INSERT INTO todolist(title, uid, completed, datetime) VALUES (?, ?, 0, ?)"
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(sql, (data["title"], data["uid"], datetime.now()))
    conn.commit()
    log_query(sql)
    return jsonify({"msg": "ok"})


@app.route("/todos/<int:id>", methods=["PUT"])
def done(id):
    sql = "UPDATE todolist SET completed=1 WHERE id=?"
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    log_query(sql)
    return jsonify({"msg": "done"})


@app.route("/todos/<int:id>", methods=["DELETE"])
def delete(id):
    sql = "DELETE FROM todolist WHERE id=?"
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    log_query(sql)
    return jsonify({"msg": "deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)