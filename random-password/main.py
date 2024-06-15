from flask import Flask, render_template, jsonify
import random
import string

app = Flask(__name__)


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+[]{}|<>?"
    password = "".join(random.choice(characters) for i in range(length))
    return password


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/generate_password")
def generate_password_route():
    password = generate_password()
    return jsonify(password=password)


if __name__ == "__main__":
    app.run(debug=True)
