from flask import Flask, request, jsonify, send_file, abort
from flask_cors import CORS

from PIL import UnidentifiedImageError

from engine.model import model
from engine.table import process_input, process_output
from engine.pdf import generate_pdf
from misc.util import get_temp_file_path


app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def index():
    return "I <3 Scarlett"


@app.route("/file", methods=["POST"])
def file():
    try:
        request.files.getlist("file")[0].save(input_file_path := get_temp_file_path("xlsx"))
    except IndexError as e:
        print(e)
        return abort(406, "Must contain a file")

    try:
        input_data = process_input(input_file_path)
    except Exception as e:
        print(e)
        return abort(406, "Bad file")

    contents = {key: [] for key in ("requirements", "conditions", "notes")}
    for text in input_data:
        for key, value in model.predict(text).items():
            contents[key].append(value)

    return send_file(
        process_output(contents),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=False,
        download_name="result.xlsx"
    )


@app.route("/pdf", methods=["POST"])
def json():
    try:
        kwargs: dict[str, ...] = request.form.to_dict()

        kwargs.update(model.predict(kwargs["description"]))
        kwargs.pop("description")

        if request.files:
            kwargs["image_path"] = get_temp_file_path(request.files.getlist("file")[0].filename.split(".")[-1])
            request.files.getlist("file")[0].save(kwargs["image_path"])

        kwargs.pop("file", None)

        pdf_path = generate_pdf(**kwargs)
    except (TypeError, KeyError) as e:
        print(e)
        return abort(406, "Wrong input")
    except UnidentifiedImageError:
        return abort(406, "Wrong file type")

    return send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=False,
        download_name="job_description.pdf"
    )


@app.route("/api", methods=["POST"])
def api():
    return jsonify(model.predict(request.json["text"]))


if __name__ == "__main__":
    app.run("localhost", 1535)
