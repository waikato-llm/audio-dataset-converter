import argparse
import librosa
import numpy as np
import soundfile as sf
from typing import List

from wai.logging import LOGGING_WARNING

from seppl.variables import VariableSupporter, variable_list, expand_variables
from kasperl.api import StreamWriter, make_list
from adc.api import AudioData, FORMAT_WAV


class MergedWriter(StreamWriter, VariableSupporter):

    def __init__(self, audio_file: str = None, annotations_file: str = None, separator: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param audio_file: the output wav file to save the audio to
        :type audio_file: str
        :param annotations_file: the file to store the annotations in, ignored if None
        :type annotations_file: str
        :param separator: the separator to use for combining the annotations, use \n and \t for newline and tab
        :type separator: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.audio_file = audio_file
        self.annotations_file = annotations_file
        self.separator = separator
        self._audio = None
        self._sample_rate = None
        self._annotations = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-merged"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Merges the audio and saves it in WAV format. Optionally merges the annotations as well. NB: stores the audio in memory before writing it out to disk when the pipeline finishes up."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-a", "--audio", type=str, help="The WAV file to store the merged audio in. " + variable_list(obj=self), required=True)
        parser.add_argument("-A", "--annotations", type=str, help="The text file to store the merged annotations in. " + variable_list(obj=self), required=False, default=None)
        parser.add_argument("-s", "--separator", type=str, help="The separator to use when merging annotations, use \\n and \\t for newline and separator.", required=False, default=" ")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.audio_file = ns.audio
        self.annotations_file = ns.annotations
        self.separator = ns.separator

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
        if self.audio_file is None:
            raise Exception("No audio file specified!")
        if self.separator is None:
            self.separator = " "
        self._audio = []
        self._sample_rate = None
        if self.annotations_file is not None:
            self._annotations = []

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            audio = item.audio
            if self._sample_rate is None:
                self._sample_rate = item.sample_rate
            elif item.sample_rate != self._sample_rate:
                self.logger().warning("Resampling audio from %d to %d: %s" % (item.sample_rate, self._sample_rate, item.audio_name))
                audio = librosa.resample(audio, orig_sr=item.sample_rate, target_sr=self._sample_rate)
            self._audio.append(audio)
            if self.annotations_file is not None:
                self._annotations.append(str(item.annotation))

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()

        # save audio
        path = expand_variables(self.audio_file)
        self.logger().info("Saving merged audio to: %s" % path)
        merged = np.concatenate(self._audio)
        with open(path, "wb") as fp:
            sf.write(fp, merged, self._sample_rate, format=FORMAT_WAV)

        # save annotations?
        if self._annotations is not None:
            path = expand_variables(self.annotations_file)
            self.logger().info("Saving merged annotations to: %s" % path)
            separator = self.separator.replace("\\n", "\n").replace("\\t", "\t")
            with open(path, "w") as fp:
                fp.write(separator.join(self._annotations))
                fp.write("\n")
