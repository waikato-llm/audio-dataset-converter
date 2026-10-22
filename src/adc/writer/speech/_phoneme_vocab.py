import argparse
import json
from collections import OrderedDict, Counter
from typing import List

from kasperl.api import StreamWriter, make_list
from seppl.variables import VariableSupporter, variable_list, expand_variables
from wai.logging import LOGGING_WARNING

from adc.api import SpeechData


class PhonemeVocabularyWriter(StreamWriter, VariableSupporter):

    def __init__(self, output_file: str = None, space_separated: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the JSON output file to save the vocabulary to
        :type output_file: str
        :param space_separated: whether the phonemes are separated with single-space and words with double-space or treated as single-character
        :type space_separated: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.space_separated = space_separated
        self._phonemes = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-phoneme-vocab"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Generates a phoneme vocabulary from the collected phonemes."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output_file", type=str, help="The JSON file to write the vocabulary to; uses stdout if omitted. " + variable_list(obj=self), required=False, default=None)
        parser.add_argument("-s", "--space_separated", action="store_true", help="Whether the phonemes are separated with single-space and words with double-space or treated as single-character.")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output_file
        self.space_separated = ns.space_separated

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [SpeechData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._phonemes = Counter()
        if self.space_separated is None:
            self.space_separated = False

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            if isinstance(item, SpeechData):
                if self.space_separated:
                    chars = item.annotation.split()
                else:
                    chars = item.annotation
                self._phonemes.update(chars)

    def output_vocabulary(self):
        """
        Generates and outputs the vocabulary.
        """
        # generate vocabulary
        vocab = OrderedDict()
        vocab["<pad>"] = 0
        vocab["<unk>"] = 1
        current_id = len(vocab)
        for phoneme in sorted(self._phonemes.keys()):
            if phoneme not in vocab:
                vocab[phoneme] = current_id
                current_id += 1

        # output vocabulary
        if self.output_file is not None:
            path = expand_variables(self.output_file)
            self.logger().info("Writing phoneme vocabulary to: %s" % path)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(vocab, f, ensure_ascii=False, indent=2)
        else:
            for key in vocab:
                print("%s: %d" % (key, vocab[key]))

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.output_vocabulary()
