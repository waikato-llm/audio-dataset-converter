import argparse
import os
from typing import List, Iterable, Union

from seppl.io import locate_files
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from wai.logging import LOGGING_WARNING

from kasperl.api import Reader
from adc.api import SpeechData, locate_audio


class TxtSpeechReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 rel_path: str = None, speaker_suffix: str = None, speaker_key: str = None, resume_from: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param rel_path: the path for the audio files relative to the text files
        :type rel_path: str
        :param speaker_suffix: the file suffix for the files containing the speaker name (incl dot)
        :type speaker_suffix: str
        :param speaker_key: the key for the speaker name/id in the meta-data
        :type speaker_key: str
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
        self.rel_path = rel_path
        self.speaker_suffix = speaker_suffix
        self.speaker_key = speaker_key
        self.resume_from = resume_from
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-txt-sp"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the transcript from the associated .txt file. Speaker information can be loaded from a companion file by supplying a speaker suffix."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the .txt file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the .txt files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.txt'", required=False)
        parser.add_argument("--rel_path", type=str, help="The relative path to the audio files.", required=False, default=".")
        parser.add_argument("--speaker_suffix", type=str, help="The file suffix for the companion files that contains the speaker, e.g., '.speaker'.", required=False, default=None)
        parser.add_argument("--speaker_key", type=str, help="The key in the meta-data with the speaker name/ID.", required=False, default="speaker")
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
        self.rel_path = ns.rel_path
        self.speaker_suffix = ns.speaker_suffix
        self.speaker_key = ns.speaker_key
        self.resume_from = ns.resume_from

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [SpeechData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._inputs = None
        if self.rel_path is None:
            self.rel_path = "."
        if self.speaker_key is None:
            self.speaker_key = "speaker"

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        if self._inputs is None:
            self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.txt", resume_from=self.resume_from)
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))
        with open(self.session.current_input, "r") as fp:
            transcript = "".join(fp.readlines()).strip()

        audio = locate_audio(self._current_input, rel_path=self.rel_path)
        if audio is None:
            self.logger().warning("No associated audio file found: %s" % self._current_input)
            yield None

        # speaker present?
        speaker = None
        if self.speaker_suffix is not None:
            path = os.path.splitext(self._current_input)[0] + self.speaker_suffix
            if os.path.exists(path):
                self.logger().info("Reader speaker: %s" % path)
                with open(path, "r") as fp:
                    speaker = "".join(fp.readlines()).strip()
            else:
                self.logger().warning("Speaker file not found: %s" % path)

        result = SpeechData(source=audio, annotation=transcript)
        if speaker is not None:
            result.set_metadata({
                self.speaker_key: speaker
            })
        yield result

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return (self._inputs is not None) and len(self._inputs) == 0
