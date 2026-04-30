from flask import Flask, render_template, request, session, redirect, url_for
from questions import questions

app = Flask(__name__)
app.secret_key = "quiz_secret_key"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/start/<category>")
def start(category):

    if category not in questions:
        return "Invalid category", 404

    session["category"] = category
    session["score"] = 0
    session["q_index"] = 0
    session["wrong"] = []

    session["quiz"] = questions[category]

    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    quiz = session.get("quiz", [])
    index = session.get("q_index", 0)

    if not quiz:
        return redirect(url_for("home"))

    if index >= len(quiz):
        return redirect(url_for("result"))

    question_data = quiz[index]

    if request.method == "POST":
        selected = request.form.get("answer")
        correct = question_data["answer"]

        # store wrong answers
        if selected != correct:
            wrong = session.get("wrong", [])
            wrong.append({
                "question": question_data["question"],
                "selected": selected,
                "correct": correct
            })
            session["wrong"] = wrong
        else:
            session["score"] += 1

        session["q_index"] += 1
        return redirect(url_for("quiz"))

    return render_template(
        "quiz.html",
        question=question_data,
        index=index + 1,
        total=len(quiz)
    )


@app.route("/result")
def result():
    return render_template(
        "result.html",
        score=session.get("score", 0),
        wrong=session.get("wrong", [])
    )


if __name__ == "__main__":
    app.run(debug=True)