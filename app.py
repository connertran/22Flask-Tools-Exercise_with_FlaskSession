from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "chicken123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_homepage():
  question_number = 0
  return render_template('homepage.html', survey_title = surveys.satisfaction_survey.title, survey_instructions = surveys.satisfaction_survey.instructions, question_number=question_number)

@app.route('/answer',methods=["POST"])
def append_ans_to_res():
  choice = request.form['answer']
  responses.append(choice)
  print(responses)
  if len(responses)== len(surveys.satisfaction_survey.questions):
    return redirect('/thank-you')
  else:
    return redirect(f"/questions/{len(responses)}")

@app.route('/thank-you')
def thank_the_user():
  return render_template('complete.html')

# @app.route('/questions/<int:num>')
# def show_user_the_right_question(num):
  
#   answers_in_responses = len(responses)
#   if num <= answers_in_responses:  
#     return render_template(f'question.html', question_num = num, question = surveys.satisfaction_survey.questions[num].question, choices = surveys.satisfaction_survey.questions[num].choices)
#   elif len(surveys.satisfaction_survey.questions) == answers_in_responses:
#         # They've answered all the questions! Thank them.
#         return redirect("/thank-you")
#   else:
#     flash(f"You're trying to access an invalid question {num}")
#     return render_template('question.html', question_num = answers_in_responses,question = surveys.satisfaction_survey.questions[answers_in_responses].question, choices = surveys.satisfaction_survey.questions[answers_in_responses].choices)
@app.route('/questions/<int:num>')
def show_user_the_right_question(num):
    global responses

    answers_in_responses = len(responses)
    if num <= answers_in_responses and len(surveys.satisfaction_survey.questions) != answers_in_responses:
        return render_template(
            'question.html',
            question_num=num,
            question=surveys.satisfaction_survey.questions[num].question,
            choices=surveys.satisfaction_survey.questions[num].choices
        )
    elif len(surveys.satisfaction_survey.questions) == answers_in_responses:
        # They've answered all the questions! Thank them.
        # reset the survey
        responses = []  # Reset the global variable
        return redirect("/thank-you")
    else:
        flash(f"You're trying to access an invalid question {num}")
        return render_template(
            'question.html',
            question_num=answers_in_responses,
            question=surveys.satisfaction_survey.questions[answers_in_responses].question,
            choices=surveys.satisfaction_survey.questions[answers_in_responses].choices
        )