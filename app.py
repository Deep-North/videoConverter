import os
import traceback

from flask import Flask, request, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename, redirect

from utils.videoProcessing import transcoding
import setup as S

UPLOAD_VIDEO_FOLDER = S.UPLOAD_VIDEO_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_VIDEO_FOLDER
ALLOWED_EXTENSIONS = S.ALLOWED_EXTENSIONS


def _allowed_file(filename):
    # Проверяю расширение файла (видео это или нет)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth == S.X_Api_Key:
        return redirect('/upload_video')
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401


@app.route('/upload_video', methods=['GET'])
# Создаю примитивный web-интерфейс для проверки работы сервиса
# Предусмотрен выбор параметров: Разрешение видео, Битрейт, Кодек и Профиль кодека
# Если делать по-нормальному, то нужно рендерить темплэйт вместо этой заглушки
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
        # Получаю из запроса переданные парамтры
        file = request.files['file']
        Scale = request.values['Scale']
        Bitrate = request.values['Bitrate']
        Codec = request.values['Codec']
        Profile = request.values['Profile']

        if file and _allowed_file(file.filename):
            # Если файл подходит, то скачиваю его на сервер
            filename = secure_filename(file.filename)
            path_to_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.isdir(UPLOAD_VIDEO_FOLDER):
                os.makedirs(UPLOAD_VIDEO_FOLDER)
            try:
                file.save(path_to_file)
                if not os.path.isdir(S.CONVERTED_VIDEO_FOLDER):
                    os.makedirs(S.CONVERTED_VIDEO_FOLDER)
                path_to_converted_file = os.path.join(S.CONVERTED_VIDEO_FOLDER, filename)
                transcoder_answer = transcoding(path_to_file, path_to_converted_file, Profile, Scale, Bitrate, Codec)
                if transcoder_answer != 'ok':
                    return jsonify(transcoder_answer) # Возвращаю текст ошибки транскодирования
                return jsonify('http://127.0.0.1:5000' + url_for('uploaded_file', filename=filename))
            except:
                print('Ошибка:\n', traceback.format_exc())
                return jsonify(traceback.format_exc())

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run()