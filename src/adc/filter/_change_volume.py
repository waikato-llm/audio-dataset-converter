import argparse
from typing import List

from kasperl.api import make_list, flatten_list
from seppl.io import BatchFilter
from wai.logging import LOGGING_WARNING

from adc.api import AudioData, AudioClassificationData, SpeechData


class ChangeVolume(BatchFilter):
    """
    Changes the volume using the supplied factor.
    """

    def __init__(self, factor: float = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param factor: the factor to apply to the audio
        :type factor: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.factor = factor

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "change-volume"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Changes the volume using the supplied factor."

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
        parser.add_argument("-f", "--factor", type=float, help="The factor to apply to the audio.", default=1.0, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.factor = ns.factor

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.factor is None:
            self.factor = 1.0

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            if self.factor == 1.0:
                result.append(item)
            else:
                self.logger().info("Applying factor %f: %s" % (self.factor, item.audio_name))
                audio_new = item.audio * self.factor
                item_new = type(item)(audio_name=item.audio_name, data=item.data, audio=audio_new,
                                      audio_format=item.audio_format, duration=item.duration,
                                      sample_rate=item.sample_rate, metadata=item.get_metadata(),
                                      annotation=item.annotation)
                result.append(item_new)

        return flatten_list(result)
