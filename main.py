from flask import Flask, request, make_response
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

FILES_FOLDER = "static/files"
os.makedirs(FILES_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # receive a file and convert to pdf, return path
        file = request.files['file']

        # filename
        filename = file.filename
        file_path = FILES_FOLDER + "/" + filename
        # save file
        file.save(file_path)
        os.system(f"lowriter --headless --convert-to pdf {file_path}")

        # replace extension
        pdf_path = file_path.replace(".docx", ".pdf")

        return make_response({
            "url" : request.url_root + pdf_path,
            "files" : os.listdir(os.getcwd()),
            "files_all" : os.listdir(FILES_FOLDER)
        })
    except Exception as e:
        return make_response(str(e), 500)