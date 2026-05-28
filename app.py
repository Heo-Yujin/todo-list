from flask import Flask, request, jsonify, render_template, session
import sqlite3
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "todo_secret_key"

DB = "todo.db"


# =========================
# SQLite 연결
# =========================
def db_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# SQLite 자동 생성
# =========================
def init_sqlite():
    conn = db_conn()
    cur = conn.cursor()

    # member 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS member (
        idx INTEGER PRIMARY KEY AUTOINCREMENT,
        uname TEXT,
        uid TEXT UNIQUE,
        upwd TEXT,
        datetime TEXT
    )
    """)

    # todolist 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS todolist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        uid TEXT,
        completed INTEGER DEFAULT 0,
        datetime TEXT
    )
    """)

    conn.commit()
    conn.close()


# =========================
# MySQL 로그 초기화
# =========================
def init_mysql():
    conn = mysql.connector.connect(
        host="MYSQL_IP",
        user="admin",
        password="1234"
    )

    cur = conn.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS logdb")
    cur.execute("USE logdb")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS query_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type VARCHAR(20),
        sql_text TEXT,
        datetime DATETIME
    )
    """)

    conn.commit()
    conn.close()


# =========================
# SQL 로그 저장
# =========================
def log_query(sql):
    try:
        conn = mysql.connector.connect(
            host="MYSQL_IP",
            user="admin",
            password="1234",
            database="logdb"
        )

        cur = conn.cursor()

        qtype = sql.strip().split()[0].lower()

        cur.execute("""
            INSERT INTO query_log (type, sql_text, datetime)
            VALUES (%s, %s, %s)
        """, (qtype, sql, datetime.now()))

        conn.commit()
        conn.close()

    except Exception as e:
        print("log error:", e)


# =========================
# 메인 페이지
# =========================
@app.route("/")
def index():
    return render_template("index.html")


# =========================
# 로그인
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = db_conn()
    cur = conn.cursor()

    sql = "SELECT * FROM member WHERE uid=? AND upwd=?"
    cur.execute(sql, (data["uid"], data["upwd"]))
    user = cur.fetchone()

    log_query(sql)

    if user:
        session["uid"] = data["uid"]
        return jsonify({"msg": "login success"})
    else:
        return jsonify({"msg": "login fail"}), 401


# =========================
# Todo 조회
# =========================
@app.route("/todos", methods=["GET"])
def get_todos():
    conn = db_conn()
    cur = conn.cursor()

    sql = "SELECT * FROM todolist"
    cur.execute(sql)
    rows = cur.fetchall()

    log_query(sql)

    return jsonify([dict(r) for r in rows])


# =========================
# Todo 추가
# =========================
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json

    sql = "INSERT INTO todolist(title, uid, completed, datetime) VALUES (?, ?, 0, ?)"

    conn = db_conn()
    cur = conn.cursor()

    cur.execute(sql, (data["title"], data["uid"], datetime.now()))
    conn.commit()

    log_query(sql)

    return jsonify({"msg": "created"})


# =========================
# 완료 처리
# =========================
@app.route("/todos/<int:id>", methods=["PUT"])
def done_todo(id):
    sql = "UPDATE todolist SET completed=1 WHERE id=?"

    conn = db_conn()
    cur = conn.cursor()

    cur.execute(sql, (id,))
    conn.commit()

    log_query(sql)

    return jsonify({"msg": "updated"})


# =========================
# 삭제
# =========================
@app.route("/todos/<int:id>", methods=["DELETE"])
def delete_todo(id):
    sql = "DELETE FROM todolist WHERE id=?"

    conn = db_conn()
    cur = conn.cursor()

    cur.execute(sql, (id,))
    conn.commit()

    log_query(sql)

    return jsonify({"msg": "deleted"})


# =========================
# 실행
# =========================
if __name__ == "__main__":
    init_sqlite()
    init_mysql()
    app.run(host="0.0.0.0", port=5000)