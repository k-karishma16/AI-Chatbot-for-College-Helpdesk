from flask import Flask, render_template, request, jsonify, redirect, session
from chatbot import get_response
from database import init_db, save_chat, add_faq, get_all_faqs
from config import SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize database
init_db()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"response": "Please type a message."})

        user_message = data["message"].strip()

        if not user_message:
            return jsonify({"response": "Message cannot be empty."})

        bot_response = get_response(user_message)

        # Save chat history
        save_chat(user_message, bot_response)

        return jsonify({"response": bot_response})

    except Exception as e:
        print("Chat Error:", e)
        return jsonify({"response": "Sorry, something went wrong."})


# Admin Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


# Admin Panel
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")

    return render_template("admin.html")


# Get FAQs
@app.route("/faqs")
def faqs():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(get_all_faqs())


# Add FAQ
@app.route("/add_faq", methods=["POST"])
def add_new_faq():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.get_json()

        question = data.get("question", "").strip()
        answer = data.get("answer", "").strip()

        if not question or not answer:
            return jsonify({"message": "Question and answer required"}), 400

        add_faq(question, answer)

        return jsonify({"message": "FAQ added successfully"})

    except Exception as e:
        print("Add FAQ Error:", e)
        return jsonify({"message": "Error adding FAQ"}), 500


if __name__ == "__main__":
    app.run(debug=True)
