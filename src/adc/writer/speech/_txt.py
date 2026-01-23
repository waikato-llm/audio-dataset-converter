import argparse
import os
from typing import List

from wai.logging import LOGGING_WARNING

from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter
from kasperl.api import SplittableStreamWriter, make_list, AnnotationsOnlyWriter, add_annotations_only_writer_param
from adc.api import SpeechData


class TxtSpeechWriter(SplittableStreamWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, annotations_only: bool = None,
                 speaker_suffix: str = None, speaker_key: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the audio file/txt in
        :type output_dir: str
        :param annotations_only: whether to output only the annotations and not the images
        :type annotations_only: bool
        :param speaker_suffix: the file suffix for the files containing the speaker name (incl dot)
        :type speaker_suffix: str
        :param speaker_key: the key for the speaker name/id in the meta-data
        :type speaker_key: str
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
        self.output_dir = output_dir
        self.annotations_only = annotations_only
        self.speaker_suffix = speaker_suffix
        self.speaker_key = speaker_key

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-txt-sp"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the transcript in a .txt file alongside the audio file. If a speaker suffix is defined, then available speaker information gets stored in an additional companion file."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the audio/.txt files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        add_annotations_only_writer_param(parser)
        parser.add_argument("--speaker_suffix", type=str, help="The file suffix for the companion files to store the speaker in, e.g., '.speaker'.", required=False, default=None)
        parser.add_argument("--speaker_key", type=str, help="The key in the meta-data with the speaker name/ID.", required=False, default="speaker")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.annotations_only = ns.annotations_only
        self.speaker_suffix = ns.speaker_suffix
        self.speaker_key = ns.speaker_key

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
        if self.annotations_only is None:
            self.annotations_only = False
        if self.speaker_key is None:
            self.speaker_key = "speaker"

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next(item=item.audio_name)
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating sub dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            path = os.path.join(sub_dir, item.audio_name)
            if not self.annotations_only:
                self.logger().info("Writing audio file to: %s" % path)
                item.save_audio(path)

            if item.has_annotation:
                path = os.path.splitext(path)[0] + ".txt"
                self.logger().info("Writing transcript to: %s" % path)
                with open(path, "w") as fp:
                    fp.write(item.annotation)
                    fp.write("\n")

            if self.speaker_suffix is not None:
                if item.has_metadata() and (self.speaker_key in item.get_metadata()):
                    path = os.path.splitext(path)[0] + self.speaker_suffix
                    self.logger().info("Writing speaker to: %s" % path)
                    with open(path, "w") as fp:
                        fp.write(item.get_metadata()[self.speaker_key])
                        fp.write("\n")
                else:
                    self.logger().warning("No speaker available from meta-data: %s" % item.audio_name)
