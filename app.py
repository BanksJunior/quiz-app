from flask import Flask, render_template, request, session, redirect, url_for
from questions import questions

app = Flask(__name__)
app.secret_key = "quiz_secret_key"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- START QUIZ ----------------
@app.route("/start/<category>")
def start(category):

    if category not in questions:
        return "Invalid category", 404

    session["category"] = category.lower().replace(" ", "_")
    session["score"] = 0
    session["q_index"] = 0
    session["wrong"] = []
    session["quiz"] = questions[category]

    return redirect(url_for("quiz"))


# ---------------- QUIZ ----------------
@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    quiz_list = session.get("quiz", [])
    index = session.get("q_index", 0)

    # 🔥 END QUIZ
    if index >= len(quiz_list):
        return redirect(url_for("result"))

    question_data = quiz_list[index]

    # ---------------- ANSWER HANDLING ----------------
    if request.method == "POST":

        selected = request.form.get("answer")
        correct = question_data["answer"]

        # 🔥 SAFE SESSION INIT (important for stability)
        session.setdefault("score", 0)
        session.setdefault("wrong", [])

        # CHECK ANSWER
        if selected == correct:
            session["score"] += 1
        else:
            session["wrong"].append({
                "question": question_data["question"],
                "selected": selected if selected else "No Answer",
                "correct": correct
            })

        # NEXT QUESTION
        session["q_index"] = index + 1
        session.modified = True

        return redirect(url_for("quiz"))

    # ---------------- RENDER QUESTION ----------------
    return render_template(
        "quiz.html",
        question=question_data,
        index=index + 1,
        total=len(quiz_list),
        category=session.get("category")
    )


# ---------------- RESULT ----------------
@app.route("/result")
def result():
    return render_template(
        "result.html",
        score=session.get("score", 0),
        wrong=session.get("wrong", []),
        category=session.get("category")
    )


if __name__ == "__main__":
    app.run(debug=True)