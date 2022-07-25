import os
from flask import Flask, render_template, redirect, flash, request, send_from_directory
from werkzeug.utils import secure_filename
from config import *
from mongopass import *
import pandas as pd
import openpyxl
import json
import csv
from flask import jsonify
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/')
@app.route('/table')
def table():

    return render_template('table.html')


@app.route("/ajaxfile", methods=["POST", "GET"])
def ajaxfile():
    if request.method == 'POST':
        draw = request.values.get('draw')
        row = request.values.get('start')
        rowperpage = request.values.get('length')
        searchValue = request.values.get("search[value]")
        print(draw)
        print(row)
        print(rowperpage)
        print(searchValue)
        totalRecords = collection.count_documents({})
        print(totalRecords)
        totalRecordwithFilter = totalRecords
        print(totalRecordwithFilter)
        table = collection.find().batch_size(totalRecordwithFilter)
        data = []
        for row in table:

            data.append({
                'index': row["index"],
                'name': row['name'],
                'date': row['date'],

                'status': row['status']
            })

        response = {
            'draw': draw,
            'iTotalRecords': totalRecords,
            'iTotalDisplayRecords': int(totalRecordwithFilter),
            'aaData': data,
        }

        return jsonify(response)


@app.route('/', methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template('upload.html')

    if not 'file' in request.files:
        flash('No file part in request')
        return redirect(request.url)

    files = request.files.getlist('file')

    for file in files:
        if file.filename == '':
            flash('No file uploaded')
            return redirect(request.url)

        if file_valid(file.filename):
            read_file = pd.read_excel(file)
            # df=pd.DataFrame(read_file)
            read_file.reset_index(inplace=True)
            data_dict = read_file.to_dict("records")
            collection.insert_many(data_dict)
            ajaxfile()
        else:
            flash('Invalid file type')
            return redirect(request.url)

    return table()


if __name__ == "__main__":
    print('to upload files navigate to http://127.0.0.1:4000/')
    app.run(host='127.0.0.1', port=4000, debug=True, threaded=True)
