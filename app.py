from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def show_home_page():
    # """Return initial page with title, instructions, and button"""
    title = survey.title
    instruction = survey.instructions
    return render_template(
        "survey_start.html",
        title=title,
        instruction=instruction
    )

@app.post("/begin")
def begin_survey():
    session["responses"] = []
    return redirect("/questions/0")


@app.get("/questions/<int:nums>")
def show_question(nums):
    """Show question"""
    question = survey.questions[nums]
    return render_template(
        "question.html",
        question=question,
        question_number=nums
    )


@app.post("/answer")
def handle_answer():
    """Save answer to global variable and redirect to next question"""
    answer = request.form["answer"]
    question_number = int(request.form["current_question"]) + 1
    response = session["response"]
    response.append(answer)
    session["response"] = response

    if len(session["response"]) == len(survey.questions):
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{question_number}")


@app.get("/thankyou")
def handle_completion():
    """Redirect user to completion page once done with survey"""
    questions_and_answers = zip(survey.questions, session["response"])
    return render_template("completion.html", questions_and_answers=questions_and_answers)
