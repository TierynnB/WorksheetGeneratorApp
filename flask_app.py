# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, send_from_directory
from utilities import *
import os
from config import DOWNLOAD_FOLDER

app = Flask(__name__)
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])  # Handle both GET and POST requests
def index():
    if request.method == "POST":  # Check if button was clicked (POST request)
        number_of_equations = request.form["number_of_equations"]
        # number_of_equations = 14
        hide_all_values = False
        hide_first_value = False
        # hide_all_values = request.form["hideAllValues"]
        # hide_first_value = request.form["hideFirstValues"]
        hide_number_random_values = request.form["hideRandomValues"]
        print(request.form)
        document = create_basic_document(
            number_of_equations,
            hide_all_values,
            hide_first_value,
            hide_number_random_values,
        )
        return render_template(
            "main_page.html", message=document
        )  # Pass message to template


@app.route("/download/<filename>")
def download_file(filename):
    uploads = os.path.join(app.root_path, app.config["DOWNLOAD_FOLDER"])
    return send_from_directory(uploads, filename, as_attachment=True)
