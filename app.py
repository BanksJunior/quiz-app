from flask import Flask, render_template, request, session, redirect, url_for
from questions import questions

app = Flask(__name__)
app.secret_key = "quiz_secret_key"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- INTRO PAGE (NEW NETFLIX STEP) ----------------
@app.route("/intro/<category>")
def intro(category):

    category = category.lower().replace(" ", "_")

    if category not in questions:
        return "Invalid category", 404

    return render_template("intro.html", category=category)


# ---------------- START QUIZ ----------------
@app.route("/start/<category>")
def start(category):

    category = category.lower().replace(" ", "_")

    if category not in questions:
        return "Invalid category", 404

    session["category"] = category
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

    # END QUIZ
    if index >= len(quiz_list):
        return redirect(url_for("result"))

    question_data = quiz_list[index]

    # ANSWER HANDLING
    if request.method == "POST":

        selected = request.form.get("answer")
        correct = question_data["answer"]

        session.setdefault("score", 0)
        session.setdefault("wrong", [])

        if selected == correct:
            session["score"] += 1
        else:
            session["wrong"].append({
                "question": question_data["question"],
                "selected": selected if selected else "No Answer",
                "correct": correct
            })

        session["q_index"] = index + 1
        session.modified = True

        return redirect(url_for("quiz"))

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