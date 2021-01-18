import datetime
import os
import traceback

from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from utils.videoProcessing import transcoding

UPLOAD_VIDEO_FOLDER = r'C:\Users\g-luc\YandexDisk\python code\videoConverter\uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_VIDEO_FOLDER
ALLOWED_EXTENSIONS = {'avi', 'mp4', 'mpg'}


def _allowed_file(filename):
    # Проверяем расширение файла (видео это или нет)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload_video', methods=['GET'])
def load_video():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>

        <select name=Scale>
            <option value="640x480">640x480</option>
            <option value="1280x720">1280x720</option>
            <option value="1920x1080">1920x1080</option>
        </select>

        <select name=Bitrate>
            <option value="1500k">1500 Kbit/s</option>
            <option value="2000k">2000 Kbit/s</option>
        </select>

        <select name=Codec>
            <option value="h264">h264</option>
            <option value="DivX">mpeg4</option>
            <option value="DivX">webp</option>
            <option value="DivX">wmv2</option>
        </select>

        <select name=Profile>
            <option value="high">high</option>
            <option value="main">low</option>
            <option value="baseline">low</option>
        </select>

        <input type=submit value=Upload>
        </p>
    </form>
    '''


@app.route('/upload_video', methods=['POST'])
def answer():
    # сохраняю видео на сервер
    if request.method == 'POST':
        file = request.files['file']
        Scale = request.values['Scale']
        Bitrate = request.values['Bitrate']
        Codec = request.values['Codec']
        Profile = request.values['Profile']

        print(file.filename)
        print(Scale, Bitrate, Codec, Profile)

        if file and _allowed_file(file.filename):
            # filename, file_extension = os.path.splitext(file)
            # filename = file.filename
            filename = secure_filename(file.filename)
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.isdir(UPLOAD_VIDEO_FOLDER):
                os.makedirs(UPLOAD_VIDEO_FOLDER)
            try:
                file.save(path_to_file)
                path_to_file1 = os.path.abspath(path_to_file)
                #path_to_file = path_to_file.replace('\\\\', '\\')
                print(path_to_file1)
                transcoding(path_to_file1, path_to_file1, Profile, Scale, Bitrate, Codec)
                #file.close()
                #return redirect(url_for('uploaded_file', filename=filename))
                return jsonify('http://127.0.0.1:5000' + url_for('uploaded_file', filename=filename))
            except:
                print('Ошибка:\n', traceback.format_exc())
            # answer = str(r'C:\Users\g-luc\YandexDisk\python code\videoConverter\videos') + '\\' + str(DATETIME) + '_' + str(filename)
            # print(answer)
            # return jsonify(answer)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run()