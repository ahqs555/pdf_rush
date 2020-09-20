import json
import os
import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='', template_folder='')
CORS(app)


@app.route('/', methods=['GET'])
def get_index():
    return '我已收到'


@app.route('/api/get_pdf_list', methods=['GET'])
def get_pdf_list():
    dir = 'pdfs'
    response_list = []
    for file in os.listdir(dir):
        file_path = os.path.join(os.getcwd(), dir, file)
        temp_dic = {'file_name': file, 'file_path': file_path}
        response_list.append(temp_dic)
    return jsonify({"pdf_file": response_list})


@app.route('/api/get_pdf_content', methods=['GET'])
def get_pdf_content():
    # pdf_id = request.args.get('pdf_id')
    dir = 'pdfs'
    file = request.args.get("file_name")
    pdf_id = os.path.join(os.getcwd(), dir, file)
    with open(pdf_id, 'rb') as f:
        blob = base64.b64encode(f.read())
    # TODO: use path to sent pdf blob to front end\
    return blob


if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    app.run(host='0.0.0.0')
