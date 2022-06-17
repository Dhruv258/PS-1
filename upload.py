import os
from flask import Flask, render_template, redirect, flash, request, send_from_directory
from werkzeug.utils import secure_filename
from config import *
from mongopass import *
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = mongopass
mongo = PyMongo(app)
db=mongo.db

@app.route('/')
def index():
  return render_template('upload.html')

@app.route('/', methods=['POST'])
def savefile():
    if 'new_file' in request.files:
        new_file = request.files['new_file']
        flash("1")
        mongo.save_file(new_file.filename, new_file)
        data = {'Name' : request.values.get('name'), 'File Name' : new_file.filename}
        db.users.insert(data)
        return()
        

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
      savefile()
    else:
      flash('Invalid file type')
      return redirect(request.url) 
      
  return "Files uploaded successfully"



if __name__ == "__main__":
    print('to upload files navigate to http://127.0.0.1:4000/upload')
    app.run(host='127.0.0.1',port=4000,debug=True,threaded=True)
