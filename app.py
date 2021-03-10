from flask import Flask, request, render_template, url_for, redirect, session
from db import db
import csv
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.before_first_request
def create_tables():
	db.create_all()


@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_csv(data):
    with open('database.csv', 'a', newline='') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        writer = csv.writer(csvfile)
        writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong!'

if __name__ == "__main__":
	db.init_app(app)
	app.run(debug=True)