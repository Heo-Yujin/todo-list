from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import mysql.connector

app = Flask(__name__)

# =========================
# SQLite 설정
# =========================
DB = "todo.db"

def db_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# MySQL 로그 함수
# =========================
def log_query(sql):
    try:
        conn = mysql.connector.connect(
            host="MySQL서버IP",   # ← 반드시 변경
            user="admin",
            password="비밀번호",  # ← 반드시 변경
            database="logdb"
        )

        cursor = conn.cursor()

        query_type = sql.strip().split()[0].lower()

        insert_sql = """
            INSERT INTO query_log (type, sql_text, datetime)
            VALUES (%s, %s, %s)
        """

        cursor.execute(insert_sql, (query_type, sql, datetime.now()))
        conn.commit()
        conn.close()

    except Exception as e:
        print("MySQL log error:", e)


# =========================
# 페이지
# =========================
@app.route("/")
def index():
    return render_template("index.html")


# =========================
# TODO 조회
# =========================
@app.route("/todos", methods=["GET"])
def get_todos():
    conn = db_conn()
    cur = conn.cursor()

    sql = "SELECT * FROM todolist"
    cur.execute(sql)
    rows = cur.fetchall()

    log_query(sql)

    return jsonify([dict(row) for row in rows])


# =========================
# TODO 추가
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
def update_todo(id):
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
    app.run(host="0.0.0.0", port=5000, debug=True)