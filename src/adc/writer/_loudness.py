import argparse
import csv
import os
import pyloudnorm as pyln
from typing import List

from wai.logging import LOGGING_WARNING

from seppl.variables import InputBasedVariableSupporter, variable_list
from kasperl.api import SplittableStreamWriter, make_list
from adc.api import AudioData


OUTPUT_TYE_LOUDNESS = "loudness"
OUTPUT_TYE_LOUDNESS_RANGE = "loudness-range"
OUTPUT_TYPES = [
    OUTPUT_TYE_LOUDNESS,
    OUTPUT_TYE_LOUDNESS_RANGE,
]


class LoudnessWriter(SplittableStreamWriter, InputBasedVariableSupporter):

    def __init__(self, output_file: str = None, output_type: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the output file to store the loudness in
        :type output_file: str
        :param output_type: the type of output to calculate
        :type output_type: str
        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param split_group: the regular expression with a single group used for keeping items in the same split, e.g., for identifying the base name of a file or the ID
        :type split_group: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(split_names=split_names, split_ratios=split_ratios, split_group=split_group, logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.output_type = output_type
        self._loudness = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-loudness"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Determines the loudness or loudness range of the audio clips and saves them to the specified CSV file."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The CSV file to store the loudness in. Any defined splits get added above the file. " + variable_list(obj=self), required=True)
        parser.add_argument("-t", "--output_type", choices=OUTPUT_TYPES, help="What to calculate and output.", required=False, default=OUTPUT_TYE_LOUDNESS)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output
        self.output_type = ns.output_type

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AudioData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._loudness = dict()
        if self.output_type is None:
            self.output_type = OUTPUT_TYE_LOUDNESS

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            out_file = self.session.expand_variables(self.output_file)
            if self.splitter is not None:
                split = self.splitter.next(item=item.audio_name)
                out_file = os.path.join(os.path.dirname(out_file), split, os.path.basename(out_file))
            out_dir = os.path.dirname(out_file)
            if not os.path.exists(out_dir):
                self.logger().info("Creating dir: %s" % out_dir)
                os.makedirs(out_dir)

            # init output
            if out_file not in self._loudness:
                if self.output_type == OUTPUT_TYE_LOUDNESS:
                    self._loudness[out_file] = [["file", "loudness"]]
                elif self.output_type == OUTPUT_TYE_LOUDNESS_RANGE:
                    self._loudness[out_file] = [["file", "loudness-range"]]
                else:
                    raise Exception("Unhandled output type: %s" % self.output_type)

            # calculate
            meter = pyln.Meter(item.sample_rate)
            if self.output_type == OUTPUT_TYE_LOUDNESS:
                loudness = meter.integrated_loudness(item.audio)
                self._loudness[out_file].append([item.audio_name, loudness])
            elif self.output_type == OUTPUT_TYE_LOUDNESS_RANGE:
                lra = meter.loudness_range(item.audio)
                self._loudness[out_file].append([item.audio_name, lra])
            else:
                raise Exception("Unhandled output type: %s" % self.output_type)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()

        if self._loudness is not None:
            for path in self._loudness:
                self.logger().info("Writing loudness to: %s" % path)
                with open(path, "w", newline="") as fp:
                    writer = csv.writer(fp)
                    writer.writerows(self._loudness[path])
