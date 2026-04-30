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

    # ✅ Safety check (prevents KeyError crash)
    if category not in questions:
        return "Invalid category", 404

    session["category"] = category
    session["score"] = 0
    session["q_index"] = 0

    session["quiz"] = questions[category]  # no shuffle (as you wanted)

    return redirect(url_for("quiz"))


# Quiz page
@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    quiz = session.get("quiz", [])
    index = session.get("q_index", 0)

    # If no quiz found (extra safety)
    if not quiz:
        return redirect(url_for("home"))

    # If finished quiz
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
    score = session.get("score", 0)
    return render_template("result.html", score=score)


if __name__ == "__main__":
    app.run(debug=True)