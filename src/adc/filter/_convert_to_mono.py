import argparse
import librosa

from typing import List

from seppl.io import BatchFilter
from wai.logging import LOGGING_WARNING
from kasperl.api import make_list, flatten_list
from adc.api import AudioData, AudioClassificationData, SpeechData


class ConvertToMono(BatchFilter):
    """
    Turns the audio into mono.
    """

    def __init__(self, force: bool = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param force: whether to force the conversion
        :type force: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.force = force

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "convert-to-mono"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Turns the audio into mono."

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
        parser.add_argument("-f", "--force", action="store_true", help="Whether to force the conversion rather than applying smart logic.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.force = ns.force

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.force is None:
            self.force = False

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            if self.force or not item.is_mono:
                self.logger().info("Converting to mono: %s" % item.audio_name)
                audio_new = librosa.to_mono(item.audio)
                item_new = type(item)(audio_name=item.audio_name, data=item.data, audio=audio_new,
                                      audio_format=item.audio_format, duration=item.duration,
                                      sample_rate=item.sample_rate, metadata=item.get_metadata(),
                                      annotation=item.annotation)
                result.append(item_new)
            else:
                result.append(item)

        return flatten_list(result)
