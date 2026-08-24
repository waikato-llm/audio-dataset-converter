import abc
import argparse
import logging
from typing import Dict, List

from seppl import Plugin, PluginWithLogging, Initializable, split_cmdline, split_args, args_to_objects
from wai.logging import LOGGING_WARNING


class Phonemizer(PluginWithLogging, Initializable, abc.ABC):

    def __init__(self, enabled: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the phonemizer.

        :param enabled: whether the plugin is enabled
        :type enabled: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.enabled = enabled

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("--disable", action="store_true", help="Whether to disable the phonemizer")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.enabled = not ns.disable

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        self.logger().info("Initializing...")
        if self.enabled is None:
            self.enabled = True

    def _can_phonemize(self, text: str) -> bool:
        """
        Checks whether the text can be phonemized.

        :param text: the string to check
        :return: True if it can be processed
        :rtype: bool
        """
        return self.enabled

    def _preprocess(self, text: str) -> str:
        """
        Hook method to apply to the text before phonemizing it.

        :param text: the text to pre-process
        :type text: str
        :return: the pre-processed text
        :rtype: str
        """
        return text

    def _do_phonemize(self, text: str) -> str:
        """
        Applies the phonemizer algorithm to the supplied string.

        :param text: the string to process
        :type text: str
        :return: the processed string
        :rtype: str
        """
        raise NotImplementedError()

    def _postprocess(self, text: str, phonemes: str) -> str:
        """
        Hook method to apply to the generated phonemes.

        :param text: the original input text
        :type text: str
        :param phonemes: the phonemes to post-process
        :type phonemes: str
        :return: the post-processed phonemes
        :rtype: str
        """
        return phonemes

    def phonemize(self, text: str) -> str:
        """
        Applies the phonemizer algorithm to the supplied string.

        :param text: the string to process
        :return: the processed string
        :rtype: str
        """
        if self._can_phonemize(text):
            if self.logger().isEnabledFor(logging.INFO):
                self.logger().info("Input: %s" % text)

            # pre-process
            text = self._preprocess(text)
            if self.logger().isEnabledFor(logging.INFO):
                self.logger().info("Preprocessed: %s" % text)

            # phonemize
            result = self._do_phonemize(text)
            if self.logger().isEnabledFor(logging.INFO):
                self.logger().info("Phonemes: %s" % result)

            # post-process
            result = self._postprocess(text, result)
            if self.logger().isEnabledFor(logging.INFO):
                self.logger().info("Post-processed phonemes: %s" % result)
        else:
            if self.logger().isEnabledFor(logging.INFO):
                self.logger().info("Cannot phonemize: %s" % text)
            result = text

        return result

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        self.logger().info("Finalizing...")

    @classmethod
    def parse_phonemizer(cls, cmdline: str, available_phonemizers: Dict[str, Plugin]) -> 'Phonemizer':
        """
        Parses the commandline and returns the phonemizer plugin.

        :param cmdline: the command-line to parse
        :type cmdline: str
        :param available_phonemizers: the phonemizers to use for parsing
        :type available_phonemizers: dict
        :return: the phonemizer plugin
        :rtype: Phonemizer
        """
        result = cls.parse_phonemizers(cmdline, available_phonemizers)
        if len(result) != 1:
            raise Exception("Expected a single phonemizer, but got: %d" % len(result))
        return result[0]

    @classmethod
    def parse_phonemizers(cls, cmdline: str, available_phonemizers: Dict[str, Plugin]) -> List['Phonemizer']:
        """
        Parses the commandline and returns the list of phonemizer plugins.

        :param cmdline: the command-line to parse
        :type cmdline: str
        :param available_phonemizers: the phonemizers to use for parsing
        :type available_phonemizers: dict
        :return: the list of phonemizer plugins
        :rtype: list
        """
        phonemizer_args = split_args(split_cmdline(cmdline), list(available_phonemizers.keys()))
        return args_to_objects(phonemizer_args, available_phonemizers)
