from flask import Flask, request, render_template, send_file
from stamp_engine import FolderEngine
import zipfile
import os
from pathlib import Path
import shutil

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
        os.remove(f.filename)
        relative_folder_path = f'./{f.filename.split(".")[0]}'
        folder_path = os.path.abspath(relative_folder_path)
        engine = FolderEngine(folder_path)
        engine.make_stamp_folders(folders_path=folder_path, move_files=True)
        shutil.make_archive("result","zip", folder_path)
        shutil.rmtree(folder_path)
        @app.after_request
        def delete(response):
            os.remove('result.zip')
            return response
        return send_file('result.zip')

# Running the app
if __name__ == '__main__':
    app.run(debug = False)