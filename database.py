import json
import os
import psycopg2
from urllib.parse import urlparse

TASKS_FILE = "tasks_log.json"
DATABASE_URL = os.environ.get("DATABASE_URL")  # رابط قاعدة بيانات PostgreSQL السحابية

def get_db_connection():
    if not DATABASE_URL:
        return None
    url = urlparse(DATABASE_URL)
    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

def init_db():
    # تهيئة محلية كخيار احتياطي
    if not os.path.exists(TASKS_FILE):
        initial_data = {
            "company_name": "Nadrai Dev Studio HQ",
            "ceo_status": "Active 🟢",
            "employees": [
                {"id": 1, "name": "CEO Agent", "role": "Executive", "level": 10, "xp": 450, "status": "Idle", "lamp": "🟢"},
                {"id": 2, "name": "Backend Python Agent", "role": "Development", "level": 5, "xp": 120, "status": "Idle", "lamp": "⚪"},
                {"id": 3, "name": "Code Reviewer Agent", "role": "QA & Security", "level": 7, "xp": 280, "status": "Idle", "lamp": "⚪"},
                {"id": 4, "name": "GitHub Research Agent", "role": "R&D", "level": 4, "xp": 90, "status": "Idle", "lamp": "⚪"}
            ],
            "tasks": []
        }
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=4)
            
    # إنشاء الجداول إذا كانت قاعدة بيانات PostgreSQL متصلة
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS company_state (
                    id SERIAL PRIMARY KEY,
                    data JSONB
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"خطأ في تهيئة قاعدة البيانات السحابية: {e}")

def load_data():
    init_db()
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT data FROM company_state ORDER BY id DESC LIMIT 1;")
            row = cur.fetchone()
            cur.close()
            conn.close()
            if row:
                return row[0]
        except Exception:
            pass
            
    # قراءة من الملف المحلي إذا لم تتوفر السحابية
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM company_state;") # تحديث الحالة العامة
            cur.execute("INSERT INTO company_state (data) VALUES (%s);", [json.dumps(data)])
            conn.commit()
            cur.close()
            conn.close()
            return
        except Exception as e:
            print(f"تعذر الحفظ في قاعدة البيانات السحابية: {e}")
            
    # حفظ محلي احتياطي
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)