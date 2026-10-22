import argparse
import librosa
import numpy as np
import os
from typing import List

from seppl.io import BatchFilter
from wai.logging import LOGGING_WARNING
from kasperl.api import make_list, flatten_list
from adc.api import AudioData, AudioClassificationData, SpeechData, FORMAT_WAV, FORMAT_EXTENSIONS


class NormalizePeak(BatchFilter):
    """
    Normalizes the peak to the specified maximum. Audio gets automatically converted to mono.
    """

    def __init__(self, target_dbfs: float = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param target_dbfs: the target dBFS to use
        :type target_dbfs: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.target_dbfs = target_dbfs

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "normalize-peak"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Normalizes the peak to the specified maximum. Audio gets automatically converted to mono."

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
        parser.add_argument("-t", "--target_dbfs", type=float, help="The target dBFS to use.", default=-3.0, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.target_dbfs = ns.target_dbfs

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.target_dbfs is None:
            self.target_dbfs = -3.0

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        # convert logarithmic decibel scale to linear scale
        target_amplitude = 10.0 ** (self.target_dbfs / 20.0)
        for item in make_list(data):
            try:
                if not item.is_mono:
                    self.logger().info("Converting to mono: %s" % item.audio_name)
                    audio_new = librosa.to_mono(item.audio)
                else:
                    audio_new = item.audio
                self.logger().info("Normalizing to %f: %s" % (self.target_dbfs, item.audio_name))
                audio_new = librosa.util.normalize(audio_new, norm=np.inf) * target_amplitude
                audio_name_new = os.path.splitext(item.audio_name)[0] + FORMAT_EXTENSIONS[FORMAT_WAV]
                item_new = type(item)(audio_name=audio_name_new, audio=audio_new,
                                      audio_format=FORMAT_WAV, duration=item.duration,
                                      sample_rate=item.sample_rate, metadata=item.get_metadata(),
                                      annotation=item.annotation)
                result.append(item_new)
            except:
                self.logger().exception("Failed to process: %s" % item.audio_name)

        return flatten_list(result)
