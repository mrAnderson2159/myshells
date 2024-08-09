import moviepy.editor as mp
from os.path import basename, splitext, abspath, join, exists
from datetime import timedelta
from utils import confirm


def video_audio_converter(filename: str, outdir: str) -> str:
    """Converts a video to an audio wav file

    :param filename: relative or absolute path to the video
    :type filename: str
    :param outdir: relative or absolute path to the output directory
    :type outdir: str
    :return: new absolute path of the video
    :rtype: str
    """
    new_name = join(abspath(outdir), splitext(basename(filename))[0] + '.wav')
    if not exists(new_name) or confirm(
        f"il file {new_name} esiste già, vuoi sovrascriverlo"
    ):
        clip = mp.VideoFileClip(filename)
        clip.audio.write_audiofile(new_name)
    return new_name

def timedelta_truncation(time: timedelta) -> timedelta:
    return time - timedelta(microseconds=time.microseconds)