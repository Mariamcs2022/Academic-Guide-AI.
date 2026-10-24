import sqlite3

from flask import json

# الاتصال بقاعدة البيانات (أو إنشاؤها إن لم تكن موجودة)
conn = sqlite3.connect("database2.db")
cursor = conn.cursor()

# إنشاء جدول الطلاب
cursor.execute("""
CREATE TABLE student_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feedback_text TEXT,
    date TEXT
)
""")

# إنشاء جدول المشرفين
cursor.execute("""
CREATE TABLE IF NOT EXISTS supervisors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT,
    lname TEXT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")

# إنشاء جدول النتائج
cursor.execute("""

CREATE TABLE resulte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resulte_text TEXT,
    date TEXT
)
""")

# إنشاء جدول العدّاد (بحيث لا نحاول إنشاؤه مرتين)
cursor.execute("""
CREATE TABLE IF NOT EXISTS counter (
    id INTEGER PRIMARY KEY,
    visits INTEGER
)
""")

# التأكد من وجود صف العدّاد (حتى لا يحدث خطأ عند التكرار)
cursor.execute("SELECT COUNT(*) FROM counter")
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute("INSERT INTO counter (id, visits) VALUES (1, 0)")

# طباعة جميع النتائج (اختياري)
cursor.execute("SELECT * FROM resulte")
rows = cursor.fetchall()
for row in rows:
    print(row)


# حفظ التغييرات
conn.commit()
conn.close()
