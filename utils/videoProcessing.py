import os
import subprocess
import traceback


def transcoding(input, output, profile, scale, bitrate, codec):

    input = input
    output = output
    scale = scale
    bitrate = bitrate
    codec = codec
    if codec == 'h264':
        profile = "-profile:v {profile}".format(profile=profile)
    else:
        profile = ''

    # Задаю параметры ffmpeg, которые были получены от пользователя.
    # Также задаю кодек и битрейт для аудио
    command = "ffmpeg -i {input} -s {scale} -vcodec {codec} {profile} -b:a {bitrate} -ab 320k -ar 24000 " \
              "-acodec aac -y {output}".format(input=input, scale=scale, codec=codec, profile=profile,
                                               bitrate=bitrate, output=output)
    try:
        subprocess.call(command, shell=False) # Запускаю транскодирование
        os.replace(output, input) # Заменяю загруженный файл на транскодированный. Можно и не заменять, но тогда
        # нужно будет прописать к нему путь, т.е. задать маршрут как в @app.route('/uploads/<filename>') в app.py
        message = 'ok'
    except:
        print('Ошибка:\n', traceback.format_exc())
        message = traceback.format_exc()

    return(message)


if __name__ == '__main__':
    transcoding(r'C:\Users\g-luc\Videos\123.mp4', r'C:\Users\g-luc\Videos\321.mp4', 'high', '1280x720', '1500k', 'h264')
