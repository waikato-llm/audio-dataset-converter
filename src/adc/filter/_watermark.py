import argparse
from typing import List

from kasperl.api import make_list, flatten_list
from seppl.io import BatchFilter
from wai.logging import LOGGING_WARNING

from adc.api import AudioData, Watermarker
from adc.watermarker import PassThrough


class Watermark(BatchFilter):
    """
    Applies the specified watermarker plugin to the audio data.
    """

    def __init__(self, watermarker: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param watermarker: the watermarker command line
        :type watermarker: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.watermarker = watermarker
        self._watermarker = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "watermark"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Applies the specified watermarker plugin to the audio data."

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
        return [AudioData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-p", "--watermarker", type=str, help="The watermarker command to use.", default=PassThrough().name(), required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.watermarker = ns.watermarker

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.watermarker is None:
            self.watermarker = PassThrough().name()
        from adc.registry import available_watermarkers
        self._watermarker = Watermarker.parse_watermarker(self.watermarker, available_watermarkers())

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            item_new = self._watermarker.watermark(item)
            self.logger().info("watermarked: %s" % item_new)
            result.append(item_new)

        return flatten_list(result)
