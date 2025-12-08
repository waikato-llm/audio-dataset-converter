import argparse
import os
from typing import List, Iterable

from kasperl.api import SplittableBatchWriter, AnnotationsOnlyWriter, add_annotations_only_writer_param
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter
from wai.logging import LOGGING_WARNING

from adc.api import SpeechData, FORMAT_WAV, FORMAT_EXTENSIONS


class PiperSpeechWriter(SplittableBatchWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, metadata: str = None, rel_path: str = None, speaker_key: str = None,
                 annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the audio file/annotations in
        :type output_dir: str
        :param metadata: the name of the meta-data file to use
        :type metadata: str
        :param rel_path: the path for the audio files relative to the annotation file
        :type rel_path: str
        :param speaker_key: the key for the speaker name/id in the meta-data
        :type speaker_key: str
        :param annotations_only: whether to output only the annotations and not the images
        :type annotations_only: bool
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
        self.metadata = metadata
        self.speaker_key = speaker_key
        self.rel_path = rel_path
        self.annotations_only = annotations_only
        self._splits = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-piper-sp"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the speech data in Piper format (https://github.com/rhasspy/piper/blob/master/TRAINING.md#dataset-format). If no speaker key is specified, assumes the data to be single-speaker."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the audio/metadata files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("--metadata", type=str, help="The name of the meta-data file.", required=False, default="metadata.csv")
        parser.add_argument("--speaker_key", type=str, help="The key in the meta-data with the speaker name/ID; assumes single-speaker data if not supplied.", required=False, default=None)
        parser.add_argument("--rel_path", type=str, help="The relative path to the audio files.", required=False, default="wav")
        add_annotations_only_writer_param(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.metadata = ns.metadata
        self.speaker_key = ns.speaker_key
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
            self.rel_path = "wav"
        if self.metadata is None:
            self.metadata = "metadata.csv"
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
                split = self.splitter.next(item=item.audio_name)
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            # write audio
            path = os.path.join(sub_dir, self.rel_path, item.audio_name)
            if not self.annotations_only:
                if not item.audio_name.lower().endswith(FORMAT_EXTENSIONS[FORMAT_WAV]):
                    raise Exception("Audio data not in WAV! Use convert-to-wav filter!")
                self.logger().info("Writing audio to: %s" % path)
                item.save_audio(path, make_dirs=True)

            # append annotations
            if sub_dir not in self._splits:
                self._splits[sub_dir] = []
            if item.has_annotation():
                if self.speaker_key is None:
                    row = os.path.splitext(item.audio_name)[0] + "|" + item.annotation
                else:
                    speaker = "[unknown]"
                    if item.has_metadata() and (self.speaker_key in item.get_metadata()):
                        speaker = item.get_metadata()[self.speaker_key]
                    else:
                        self.logger().warning("Failed to locate speaker using key '%s' in meta-data: %s" % item.audio_name)
                    row = os.path.splitext(item.audio_name)[0] + "|" + str(speaker) + "|" + item.annotation
                self._splits[sub_dir].append(row)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()

        for sub_dir, annotations in self._splits.items():
            # save annotations
            path = os.path.join(sub_dir, self.metadata)
            with open(path, "w") as fp:
                for row in annotations:
                    fp.write(row)
                    fp.write("\n")
