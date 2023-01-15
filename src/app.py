from flask import Flask, request, render_template
from stamp_engine import FolderEngine
import zipfile
import os
from pathlib import Path

app = Flask(__name__)


@app.route('/', methods = ['GET','POST'])  
def main():  
    return render_template("index.html")    

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)
        data = zipfile.ZipFile(f'{f.filename}', 'r')
        data.extractall()
        relative_folder_path = f'./{f.filename.split(".")[0]}'
        folder_path = os.path.abspath(relative_folder_path)
        engine = FolderEngine(folder_path)
        engine.make_stamp_folders(folders_path=folder_path)
        return render_template("index.html", output = f'Файл обработан')  

# Running the app
if __name__ == '__main__':
    app.run(debug = False)