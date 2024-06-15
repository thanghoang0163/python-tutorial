from flask import (
    Flask,
    request,
    render_template,
    redirect,
    send_from_directory,
    flash,
)
import os
from sightengine.client import SightengineClient

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["UPLOAD_FOLDER"] = "uploads/"

client = SightengineClient("1838957940", "beRqzQC4i55NodzVzvqNS6ZoSPF2eaGB")

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = file.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            output = client.check(
                "face-attributes",
                "celebrities",
                "nudity",
                "type",
                "quality",
                "genai",
            ).set_file(filepath)

            face = output["faces"] or []

            return render_template(
                "form.html",
                filename=filename,
                attributes=face[0]["attributes"] if len(face) > 0 else "",
                celebrity=face[0]["celebrity"] if len(face) > 0 else "",
                nudity=output["nudity"],
                type=output["type"],
                quality=output["quality"],
            )
    return render_template("form.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
