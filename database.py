import sqlite3
from config import DATABASE

DB_NAME = DATABASE


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # FAQ table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)

    # Chat history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert default FAQs only if empty
    cursor.execute("SELECT COUNT(*) FROM faq")
    count = cursor.fetchone()[0]

    if count == 0:
        default_faqs = [
            ("What is fee structure?", "Please contact accounts office for fee details."),
            ("Where is library?", "Library is located in Block B and open from 9 AM to 5 PM."),
            ("When are exams?", "Exam dates will be announced on the college portal."),
            ("How to get bonafide certificate?", "Apply through admin office with request form."),
            ("Placement eligibility?", "Minimum CGPA criteria depends on company requirements.")
        ]

        cursor.executemany(
            "INSERT INTO faq (question, answer) VALUES (?, ?)",
            default_faqs
        )

    conn.commit()
    conn.close()


def get_faqs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT question, answer FROM faq")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_all_faqs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT question, answer FROM faq")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"question": q, "answer": a}
        for q, a in rows
    ]


def add_faq(question, answer):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO faq (question, answer) VALUES (?, ?)",
        (question, answer)
    )

    conn.commit()
    conn.close()


def save_chat(user_message, bot_response):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history (user_message, bot_response)
        VALUES (?, ?)
        """,
        (user_message, bot_response)
    )

    conn.commit()
    conn.close()
