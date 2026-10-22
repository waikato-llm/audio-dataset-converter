import argparse
import csv
import json
import sys
from collections import OrderedDict
from typing import List, Dict

from kasperl.api import StreamWriter, make_list
from seppl.variables import VariableSupporter, variable_list, expand_variables
from wai.logging import LOGGING_WARNING

from adc.api import SpeechData

OUTPUT_FORMAT_TEXT = "text"
OUTPUT_FORMAT_CSV = "csv"
OUTPUT_FORMAT_JSON = "json"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_TEXT,
    OUTPUT_FORMAT_CSV,
    OUTPUT_FORMAT_JSON,
]

OUTPUT_TYPE_COUNTS = "counts"
OUTPUT_TYPE_PERCENTAGES = "percentages"
OUTPUT_TYPES = [
    OUTPUT_TYPE_COUNTS,
    OUTPUT_TYPE_PERCENTAGES,
]


class PhonemeDistributionWriter(StreamWriter, VariableSupporter):

    def __init__(self, output_file: str = None, output_format: str = OUTPUT_FORMAT_TEXT, output_type: str = None,
                 space_separated: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the output file to save the label distribution to
        :type output_file: str
        :param output_format: the format for the output file
        :type output_format: str
        :param output_type: how to output the distribution
        :type output_type: str
        :param space_separated: whether the phonemes are separated with single-space and words with double-space or treated as single-character
        :type space_separated: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.output_format = output_format
        self.output_type = output_type
        self.space_separated = space_separated
        self._phonemes = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-phoneme-dist"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Records the phoneme distribution and saves the statistics to the specified file."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output_file", type=str, help="The file to write the statistics to; uses stdout if omitted. " + variable_list(obj=self), required=False, default=None)
        parser.add_argument("-f", "--output_format", choices=OUTPUT_FORMATS, help="The format to use for the output.", required=False, default=OUTPUT_FORMAT_TEXT)
        parser.add_argument("-t", "--output_type", choices=OUTPUT_TYPES, help="How to output the distribution.", required=False, default=OUTPUT_TYPE_COUNTS)
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
        self.output_format = ns.output_format
        self.output_type = ns.output_type
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
        if self.output_format is None:
            self.output_format = OUTPUT_FORMAT_TEXT
        if self.output_type is None:
            self.output_type = OUTPUT_TYPE_COUNTS
        if self.space_separated is None:
            self.space_separated = False
        self._phonemes = dict()

    def add_phonemes(self, text: str):
        """
        Increments the count for the phonemes in the text.
        """
        if self.space_separated:
            chars = text.split()
        else:
            chars = text
        for char in chars:
            if char not in self._phonemes:
                self._phonemes[char] = 0
            self._phonemes[char] = self._phonemes[char] + 1

    def output_text(self, dist: Dict, keys: List, use_stdout: bool):
        """
        Outputs the label distribution in simple textual format.

        :param dist: the distribution dictionary
        :type dist: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            for k in keys:
                if self.output_type == OUTPUT_TYPE_PERCENTAGES:
                    print("%s: %f" % (k, dist[k]))
                else:
                    print("%s: %d" % (k, dist[k]))
        else:
            with open(expand_variables(self.output_file), "w") as f:
                for k in keys:
                    if self.output_type == OUTPUT_TYPE_PERCENTAGES:
                        f.write("%s: %f" % (k, dist[k]))
                    else:
                        f.write("%s: %d" % (k, dist[k]))
                    f.write("\n")

    def output_csv(self, dist: Dict, keys: List, use_stdout: bool):
        """
        Outputs the label distribution in CSV format.

        :param dist: the distribution dictionary
        :type dist: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            writer = csv.writer(sys.stdout)
            f = None
        else:
            f = open(expand_variables(self.output_file), "w")
            writer = csv.writer(f)

        writer.writerow(["Label", "Count"])
        for k in keys:
            writer.writerow([k, dist[k]])

        if f is not None:
            f.close()

    def output_json(self, dist: Dict, use_stdout: bool):
        """
        Outputs the label distribution in json format.

        :param dist: the distribution dictionary
        :type dist: dict
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            print(json.dumps(dist, indent=2))
        else:
            with open(expand_variables(self.output_file), "w") as f:
                json.dump(dist, f, indent=2)

    def output_phoneme_distribution(self):
        """
        Outputs the distribution.
        """
        keys = list(self._phonemes.keys())
        keys.sort()
        dist = OrderedDict()
        for k in keys:
            dist[k] = self._phonemes[k]

        if self.output_type == OUTPUT_TYPE_PERCENTAGES:
            total = 0
            for k in dist:
                total += dist[k]
            for k in dist:
                dist[k] = dist[k] / total * 100.0

        use_stdout = (self.output_file is None) or (len(self.output_file) == 0)

        if self.output_format == OUTPUT_FORMAT_TEXT:
            self.output_text(dist, keys, use_stdout)
        elif self.output_format == OUTPUT_FORMAT_CSV:
            self.output_csv(dist, keys, use_stdout)
        elif self.output_format == OUTPUT_FORMAT_JSON:
            self.output_json(dist, use_stdout)
        else:
            raise Exception("Unhandled output format: %s" % self.output_format)

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            if isinstance(item, SpeechData):
                self.add_phonemes(item.annotation)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.output_phoneme_distribution()
