import json
import os
import base64
import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# 数据库连接
myDatabase = sqlite3.connect('LogDB.db')
cu = myDatabase.cursor()
cu.execute("SELECT name FROM sqlite_master WHERE type='table'")
Tables = cu.fetchall()
Tables = [line[0] for line in Tables]
if 'accesslog' not in Tables:
    cu.execute("CREATE TABLE accesslog (id INTEGER PRIMARY KEY, time DEFAULT CURRENT_TIMESTAMP, userid INTEGER, contentname VARCHAR(100))")

cu.close()
myDatabase.close()

@app.route('/api/get_pdf_list', methods=['GET'])
def get_pdf_list():
    global user_id
    dir = 'pdfs'
    response_list = []
    for file in os.listdir(dir):
        # file_path = os.path.join(os.getcwd(), dir, file)
        temp_dic = {'name': file}
        response_list.append(temp_dic)
    return jsonify({"pdf_file": response_list})

@app.route('/api/get_pdf_content', methods=['GET'])
def get_pdf_content():
    # pdf_id = request.args.get('pdf_id')
    dir = 'pdfs'
    file = request.args.get("file_name")
    uid = request.args.get("user_id")
    pdf_id = os.path.join(os.getcwd(), dir, file)
    with open(pdf_id, 'rb') as f:
        blob = base64.b64encode(f.read())
    # Writing the data in to database
    myDatabase = sqlite3.connect('LogDB.db')
    cu = myDatabase.cursor()
    cu.execute('INSERT INTO accesslog (userid, contentname) VALUES (?,?)', (uid, file))
    myDatabase.commit()
    cu.close()
    myDatabase.close()

    return blob


if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    app.run(host='127.0.0.1')
