import io
import os
import tempfile
import traceback
from typing import Optional, Union, Tuple

import librosa
import numpy as np
import soundfile as sf

from kasperl.api import locate_file


def locate_audio(path: str, rel_path: str = None, suffix: str = None) -> Optional[str]:
    """
    Tries to locate the audio file (mp3 or wav) for the given path by replacing its extension.

    :param path: the base path to use
    :type path: str
    :param rel_path: the relative path to the annotation to use for looking for audio files, ignored if None
    :type rel_path: str
    :param suffix: the suffix to strip from the files, ignored if None or ""
    :type suffix: str
    :return: the located audio, None if not found
    :rtype: str
    """
    ext = [".mp3", ".MP3", ".wav", ".WAV"]
    audio_files = locate_file(path, ext, rel_path=rel_path, suffix=suffix)
    if len(audio_files) == 0:
        return None
    else:
        return audio_files[0]


def load_audio_from_file(path: str) -> Union[Tuple[np.ndarray, int], Tuple[None, None]]:
    """
    Loads the audio from the file.

    :param path: the file to load the audio from
    :type path: str
    :return: the audio data tuple (audio/np.ndarray, sample_rate/int), None if failed to load
    :rtype: tuple
    """
    try:
        return sf.read(path)
    except:
        try:
            return librosa.load(path)
        except:
            print("Failed to read: %s" % path)
            traceback.print_exc()
            return None, None


def load_audio_from_bytes(data: bytes, ext: str) -> Union[Tuple[np.ndarray, int], Tuple[None, None]]:
    """
    Loads the audio from the bytes. Falls back loading from disk, if not possible.

    :param data: the bytes to load the audio from
    :type data: bytes
    :param ext: the audio extension to use
    :type ext: str
    :return: the audio data, None if failed to load
    :rtype: np.ndarray
    """
    path = None
    try:
        buf = io.BytesIO(data)
        result = sf.read(buf)
    except:
        with tempfile.NamedTemporaryFile(suffix=ext, delete_on_close=False) as fp:
            fp.write(data)
            fp.close()
            path = fp.name
            result = load_audio_from_file(path)
    finally:
        if path is not None:
            os.remove(path)
    return result
