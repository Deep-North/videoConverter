import subprocess

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

    command = "ffmpeg -i {input} -s {scale} -vcodec {codec} {profile} -b {bitrate} -ab 320k -ar 24000 " \
              "-acodec aac -y {output}".format(input=input, scale=scale, codec=codec, profile=profile,
                                               bitrate=bitrate, output=output)
    subprocess.call(command, shell=False)


if __name__ == '__main__':
    transcoding(r'C:\Users\g-luc\Videos\123.mp4', r'C:\Users\g-luc\Videos\321.mp4', 'high', '1280x720', '1500k', 'h264')
