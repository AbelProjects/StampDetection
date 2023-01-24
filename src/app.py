from flask import Flask, request, render_template, send_file
from stamp_engine import FolderEngine
import zipfile
import os
from pathlib import Path
import shutil
import transliterate

app = Flask(__name__)


@app.route('/', methods = ['GET','POST'])  
def main():  
    return render_template("index.html")    

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)

        def unpack_zipfile(filename, extract_dir, encoding='utf8'):
            with zipfile.ZipFile(filename) as archive:
                for entry in archive.infolist():
                    name = entry.filename.encode('cp437').decode(encoding)  
                    
                    if name.startswith('/') or '..' in name:
                        continue

                    target = os.path.join(extract_dir, *name.split('/'))    
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    if not entry.is_dir(): 
                        with archive.open(entry) as source, open(target, 'wb') as dest:
                            shutil.copyfileobj(source, dest)

        unpack_zipfile(f'{f.filename}', f'./', encoding='utf8')

        os.remove(f.filename)
        relative_folder_path = f'./{f.filename.split(".")[0]}'
        folder_path = os.path.abspath(relative_folder_path)
        engine = FolderEngine(folder_path)
        engine.make_stamp_folders(folders_path=folder_path, move_files=True)
        shutil.make_archive("result","zip", folder_path)
        shutil.rmtree(folder_path)

        def stream_and_remove_file(filename):
            file_handle = open(filename, 'rb')
            yield from file_handle
            file_handle.close()
            os.remove(filename)
        
        send_file_name = transliterate.translit(f'{f.filename}', reversed=True)

        return app.response_class(
        stream_and_remove_file(filename='./result.zip'),
        headers={'Content-Type': 'application/zip', 
        'Content-Disposition': f'attachment; filename={send_file_name}'}
    )

# Running the app
if __name__ == '__main__':
    app.run(debug = False)