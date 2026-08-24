import argparse
from typing import List

from kasperl.api import make_list, flatten_list
from seppl.io import BatchFilter
from wai.logging import LOGGING_WARNING

from adc.api import SpeechData, Phonemizer
from adc.phonemizer import PassThrough


class Phonemize(BatchFilter):
    """
    Applies the specified phonemizer plugin to the speech text.
    """

    def __init__(self, phonemizer: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param phonemizer: the phonemizer command line
        :type phonemizer: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.phonemizer = phonemizer
        self._phonemizer = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "phonemize"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Applies the specified phonemizer plugin to the speech text."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [SpeechData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [SpeechData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-p", "--phonemizer", type=str, help="The phonemizer command to use.", default=PassThrough().name(), required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.phonemizer = ns.phonemizer

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.phonemizer is None:
            self.phonemizer = PassThrough().name()
        from adc.registry import available_phonemizers
        self._phonemizer = Phonemizer.parse_phonemizer(self.phonemizer, available_phonemizers())
        self._phonemizer.initialize()

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            annotation_new = self._phonemizer.phonemize(item.annotation)
            self.logger().info("phonemized: %s -> %s" % (item.annotation, annotation_new))
            item_new = item.duplicate(annotation=annotation_new)
            result.append(item_new)

        return flatten_list(result)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        if self._phonemizer is not None:
            self._phonemizer.finalize()
            self._phonemizer = None
