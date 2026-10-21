import argparse
import librosa
import numpy as np
import os
import pyloudnorm as pyln
from typing import List

from seppl.io import BatchFilter
from wai.logging import LOGGING_WARNING
from kasperl.api import make_list, flatten_list
from adc.api import AudioData, AudioClassificationData, SpeechData, FORMAT_WAV, FORMAT_EXTENSIONS


class NormalizeLoudness(BatchFilter):
    """
    Normalizes the audio to the specified target LUFS (loudness units full scale). Audio gets automatically converted to mono.
    """

    def __init__(self, target_lufs: float = None, max_peak_dbfs: float = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param target_lufs: the target LUFS to use
        :type target_lufs: float
        :param max_peak_dbfs: the maximum peak dBFS to allow
        :type max_peak_dbfs: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.target_lufs = target_lufs
        self.max_peak_dbfs = max_peak_dbfs

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "normalize-loudness"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Normalizes the audio to the specified target LUFS (loudness units full scale). Audio gets automatically converted to mono."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AudioData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [AudioClassificationData, SpeechData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-t", "--target_lufs", type=float, help="The target LUFS to use.", default=-23.0, required=False)
        parser.add_argument("-m", "--max_peak_dbfs", type=float, help="The maximum peak dBFS to allow.", default=-1.0, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.target_lufs = ns.target_lufs
        self.max_peak_dbfs = ns.max_peak_dbfs

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.target_lufs is None:
            self.target_lufs = -23.0
        if self.max_peak_dbfs is None:
            self.max_peak_dbfs = -1.0

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        max_allowed_amp = 10.0 ** (self.max_peak_dbfs / 20.0)
        for item in make_list(data):
            if not item.is_mono:
                self.logger().info("Converting to mono: %s" % item.audio_name)
                audio_new = librosa.to_mono(item.audio)
            else:
                audio_new = item.audio

            # determine loudness
            meter = pyln.Meter(item.sample_rate)
            loudness = meter.integrated_loudness(audio_new)
            # silent?
            if np.isinf(loudness):
                result.append(item)
                continue

            # normalize
            self.logger().info("Normalizing loudness %f to %f LUFS" % (loudness, self.target_lufs))
            audio_new = pyln.normalize.loudness(audio_new, loudness, self.target_lufs)

            # check peak
            current_peak = np.max(np.abs(audio_new))
            if current_peak > max_allowed_amp:
                # Scale back to prevent clipping
                audio_new = audio_new * (max_allowed_amp / current_peak)
                self.logger().info("Peak scaled down to %f dBFS to prevent clipping." % self.max_peak_dbfs)

            audio_name_new = os.path.splitext(item.audio_name)[0] + FORMAT_EXTENSIONS[FORMAT_WAV]
            item_new = type(item)(audio_name=audio_name_new, audio=audio_new,
                                  audio_format=FORMAT_WAV, duration=item.duration,
                                  sample_rate=item.sample_rate, metadata=item.get_metadata(),
                                  annotation=item.annotation)
            result.append(item_new)

        return flatten_list(result)
