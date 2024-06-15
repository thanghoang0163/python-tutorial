from flask import Flask, request, redirect, render_template, jsonify
import json
import os
import string
import random

app = Flask(__name__)
url_db_file = "urls.json"


def load_urls():
    if os.path.exists(url_db_file):
        with open(url_db_file, "r") as file:
            return json.load(file)
    return {}


def save_urls(urls):
    with open(url_db_file, "w") as file:
        json.dump(urls, file)


def generate_short_id(num_chars=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=num_chars))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form["original_url"]
        urls = load_urls()
        short_id = generate_short_id()

        while short_id in urls:
            short_id = generate_short_id()

        urls[short_id] = original_url
        save_urls(urls)

        return render_template("form.html", short_url=request.host_url + short_id)

    return render_template("form.html")


@app.route("/<short_id>")
def redirect_to_url(short_id):
    urls = load_urls()
    original_url = urls.get(short_id)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404


@app.route("/api/shorten", methods=["POST"])
def api_shorten_url():
    data = request.get_json()
    original_url = data.get("original_url")
    if not original_url:
        return jsonify({"error": "Missing 'original_url' field"}), 400

    urls = load_urls()
    short_id = generate_short_id()

    while short_id in urls:
        short_id = generate_short_id()

    urls[short_id] = original_url
    save_urls(urls)

    return jsonify({"short_url": request.host_url + short_id}), 201


if __name__ == "__main__":
    app.run(debug=True)
