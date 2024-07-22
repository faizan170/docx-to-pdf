from flask import Flask, request, make_response
from flask_cors import CORS
import os, shutil, subprocess
app = Flask(__name__)
CORS(app)

FILES_FOLDER = "static/files"
os.makedirs(FILES_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Receive a file and convert to pdf, return path
        file = request.files['file']

        # Filename
        filename = file.filename
        file_path = os.path.join(FILES_FOLDER, filename)
        # Save file
        file.save(file_path)
        pdf_path = file_path.replace(".docx", ".pdf")

        # Execute pandoc command and capture output
        command = f"pandoc {file_path} -o {pdf_path}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            return make_response({
                "error": result.stderr
            }, 500)

        return make_response({
            "url": request.url_root + pdf_path,
            "files": os.listdir(os.getcwd()),
            "files_all": os.listdir(FILES_FOLDER),
            "command_output": result.stdout,
            "command" : command
        })

    except Exception as e:
        return make_response({
            "error": str(e)
        }, 500)