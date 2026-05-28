# Todo List Project (Flask + SQLite + jQuery + MySQL Log)

## 📌 프로젝트 개요
Flask를 이용하여 만든 Todo List 웹 애플리케이션입니다.  
SQLite로 할 일을 관리하고, MySQL 서버에 모든 SQL 쿼리를 로그로 저장합니다.

---

## ⚙️ 기술 스택
- Flask (Python)
- HTML / jQuery (AJAX)
- SQLite (로컬 DB)
- MySQL (로그 DB)

---

## 📁 주요 기능

### ✔ 로그인 기능
- member 테이블 기반 로그인
- 세션(session) 사용

### ✔ Todo CRUD 기능
- 할 일 추가 (POST /todos)
- 할 일 조회 (GET /todos)
- 할 일 완료 (PUT /todos/<id>)
- 할 일 삭제 (DELETE /todos/<id>)

### ✔ 로그 기능
- 모든 SQL 실행 로그 저장
- MySQL query_log 테이블에 저장
- type / sql / datetime 기록

---

## 🗄 데이터베이스 구조

### SQLite

#### member
- idx
- uname
- uid
- upwd
- datetime

#### todolist
- id
- title
- uid
- completed
- datetime

---

### MySQL

#### query_log
- id
- type
- sql_text
- datetime

---

## 🚀 실행 방법

### 1. 가상환경 활성화
```bash
source venv312/bin/activate
```

---

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

---

### 3. 서버 실행
```bash
python app.py
```

---

### 4. 접속
```
http://localhost:5000
```

---

## 📂 프로젝트 구조

```
todo/
├── app.py
├── todo.db
├── templates/
│   └── index.html
├── static/
│   └── app.js
├── requirements.txt
└── README.md
```

---

## 🧠 특징
- REST API 구조
- AJAX 비동기 처리
- DB 자동 생성
- MySQL 로그 서버 분리
- 로그인 + CRUD 통합

---

## 👨‍💻 개발 환경
- Ubuntu Server (VirtualBox)
- Python 3.x
- Flask
- MySQL 8.x



id=admin
password=1234

db사용자 admin  비번: 1234