from flask import Flask, render_template, request, session, redirect, url_for
from questions import questions

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

# Home
@app.route("/")
def home():
    return render_template("home.html")

# Start quiz category
@app.route("/start/<category>")
def start(category):
    session["category"] = category
    session["score"] = 0
    session["q_index"] = 0

    session["quiz"] = questions[category]  # no shuffle

    return redirect(url_for("quiz"))

# Quiz page
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    quiz = session.get("quiz", [])
    index = session.get("q_index", 0)

    # If finished
    if index >= len(quiz):
        return redirect(url_for("result"))

    question_data = quiz[index]

    if request.method == "POST":
        selected = request.form.get("answer")

        if selected == question_data["answer"]:
            session["score"] += 1

        session["q_index"] += 1
        return redirect(url_for("quiz"))

    return render_template(
        "quiz.html",
        question=question_data,
        index=index + 1,
        total=len(quiz)
    )

# Result page
@app.route("/result")
def result():
    return render_template("result.html", score=session.get("score", 0))


# ✅ RAILWAY FIX (IMPORTANT)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
