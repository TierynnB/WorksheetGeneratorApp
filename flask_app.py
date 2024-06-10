# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, send_from_directory
from utilities import *
import os
from config import DOWNLOAD_FOLDER
import pypandoc

app = Flask(__name__)
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])  # Handle both GET and POST requests
def index():
    if request.method == "POST":  # Check if button was clicked (POST request)

        hide_all_values = False
        hide_first_value = False
        hide_number_random_values = 0

        number_of_equations = int(request.form.get("number_of_equations", 14))
        # hide_number_random_values = int(request.form.get("hide_random_number", 1))
        choice = request.form.get("choice")
        match choice:
            case "hideRandomValues":
                hide_number_random_values = int(
                    request.form.get("hide_random_number", 1)
                )
            case "hideFirstValue":
                hide_first_value = True
            case "hideAllValues":
                hide_all_values = True
        document = create_basic_document(
            number_of_equations,
            hide_all_values,
            hide_first_value,
            hide_number_random_values,
        )

        pypandoc.convert_file(
            "GeneratedDocuments/worksheetGenerated.docx",
            "html",
            outputfile="previewDocument.html",
        )

        process_and_save_subscripts("previewDocument.html")

        return render_template("main_page.html")


@app.route("/download/<filename>")
def download_file(filename):
    uploads = os.path.join(app.root_path, app.config["DOWNLOAD_FOLDER"])
    return send_from_directory(uploads, filename, as_attachment=True)


@app.route("/preview_document")
def serve_html():
    with open("previewDocument.html", "r") as f:
        html_content = f.read()
    return html_content
