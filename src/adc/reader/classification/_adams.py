import argparse
from typing import List, Iterable, Union

from wai.logging import LOGGING_WARNING
from wai.common.file.report import loadf
from seppl.io import locate_files
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from adc.api import AudioClassificationData, locate_audio
from adc.api import Reader


class AdamsAudioClassificationReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 class_field: str = None, resume_from: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param class_field: the name of the field containing the classification label
        :type class_field: str
        :param resume_from: the file to resume from (glob)
        :type resume_from: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.class_field = class_field
        self.resume_from = resume_from
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-adams-ac"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the audio classification from the specified class field in the associated .report file."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the report file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the report files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.report'", required=False)
        parser.add_argument("-c", "--class_field", metavar="FIELD", type=str, default=None, help="The report field containing the audio classification label", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list
        self.class_field = ns.class_field
        self.resume_from = ns.resume_from

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [AudioClassificationData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.class_field is None:
            raise Exception("No class field defined!")
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.report", resume_from=self.resume_from)

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))
        report = loadf(self._current_input)

        meta = dict()
        for field in report:
            meta[field.to_parseable_string()] = report.get_value(field)
        if len(meta) == 0:
            meta = None

        audio = locate_audio(self._current_input)
        if audio is None:
            self.logger().warning("No associated audio file found: %s" % self._current_input)
            yield None

        if report.has_value(self.class_field):
            yield AudioClassificationData(source=audio, annotation=report.get_string_value(self.class_field), metadata=meta)
        else:
            yield AudioClassificationData(source=audio, metadata=meta)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
