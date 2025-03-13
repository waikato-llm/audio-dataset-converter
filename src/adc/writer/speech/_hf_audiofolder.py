import argparse
import csv
import os
from typing import List, Iterable

from wai.logging import LOGGING_WARNING

from adc.api import SpeechData, SplittableBatchWriter, AnnotationsOnlyWriter, add_annotations_only_param
from adc.reader.speech import HF_AUDIOFOLDER_EXPECTED_HEADER
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


class HuggingFaceAudioFolderSpeechWriter(SplittableBatchWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, rel_path: str = None, annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the audio file/annotations in
        :type output_dir: str
        :param rel_path: the path for the audio files relative to the annotation file
        :type rel_path: str
        :param annotations_only: whether to output only the annotations and not the images
        :type annotations_only: bool
        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(split_names=split_names, split_ratios=split_ratios, logger_name=logger_name, logging_level=logging_level)
        self.output_dir = output_dir
        self.rel_path = rel_path
        self.annotations_only = annotations_only
        self._splits = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-hf-audiofolder-sp"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the speech data in the Huggingface AudioFolder format (https://huggingface.co/docs/datasets/audio_dataset#audiofolder)."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the data. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("--rel_path", type=str, help="The relative path to the audio files.", required=False, default=".")
        add_annotations_only_param(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.rel_path = ns.rel_path
        self.annotations_only = ns.annotations_only

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

        if self.rel_path is None:
            self.rel_path = "."
        if self.annotations_only is None:
            self.annotations_only = False
        self._splits = dict()

    def write_batch(self, data: Iterable):
        """
        Saves the data in one go.

        :param data: the data to write
        :type data: Iterable
        """
        for item in data:
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next()
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            # write audio
            path = os.path.join(sub_dir, self.rel_path, item.audio_name)
            if not self.annotations_only:
                self.logger().info("Writing audio to: %s" % path)
                item.save_audio(path)

            # append annotations
            if sub_dir not in self._splits:
                self._splits[sub_dir] = []
            file_name = item.audio_name
            if (len(self.rel_path) > 0) and (self.rel_path != "."):
                file_name = self.rel_path + "/" + file_name
            if item.has_annotation():
                row = {
                    "file_name": file_name,
                    "transcription": item.annotation,
                }
                self._splits[sub_dir].append(row)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()

        for sub_dir, annotations in self._splits.items():
            # save annotations
            path = os.path.join(sub_dir, "metadata.csv")
            with open(path, "w") as fp:
                csv_writer = csv.DictWriter(fp, HF_AUDIOFOLDER_EXPECTED_HEADER.split(","))
                csv_writer.writeheader()
                for row in annotations:
                    csv_writer.writerow(row)
