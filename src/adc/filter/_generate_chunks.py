import argparse
import os
from typing import List

from kasperl.api import make_list, flatten_list, safe_deepcopy
from seppl.io import BatchFilter
from wai.logging import LOGGING_WARNING

from adc.api import AudioData, AudioClassificationData, SpeechData, FORMAT_WAV, FORMAT_EXTENSIONS


class GenerateChunks(BatchFilter):
    """
    Splits the audio into chunks of the specified length.
    """

    def __init__(self, length: float = None, metadata_key: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param length: the length in seconds
        :type length: float
        :param metadata_key: the key in the meta-data for storing the offset
        :type metadata_key: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.length = length
        self.metadata_key = metadata_key

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "generate-chunks"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Splits the audio into chunks of the specified length."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AudioData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [AudioClassificationData, SpeechData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-L", "--length", type=float, help="The length of the chunks in seconds.", default=1.0, required=False)
        parser.add_argument("-k", "--metadata_key", type=str, help="The key in the meta-data to store the offset under.", default="offset", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.length = ns.length
        self.metadata_key = ns.metadata_key

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.length is None:
            self.length = 1.0
        if self.metadata_key is None:
            self.metadata_key = "offset"

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            if item.duration <= self.length:
                result.append(item)
            else:
                subset = []
                self.logger().info("Generating chunks of length %f: %s" % (self.length, item.audio_name))

                # get number of samples for "length" seconds
                buffer = int(self.length * item.sample_rate)

                audio = item.audio
                samples_total = len(audio)
                samples_written = 0
                counter = 1
                time = 0
                while samples_written < samples_total:
                    # check if the buffer is not exceeding total samples
                    if buffer > (samples_total - samples_written):
                        buffer = samples_total - samples_written
                    block = audio[samples_written: (samples_written + buffer)]
                    audio_name_new = os.path.splitext(item.audio_name)[0] + "-" + str(time) + FORMAT_EXTENSIONS[FORMAT_WAV]
                    meta_new = safe_deepcopy(item.get_metadata())
                    meta_new[self.metadata_key] = time
                    item_new = type(item)(audio_name=audio_name_new, audio=block,
                                          audio_format=FORMAT_WAV, sample_rate=item.sample_rate,
                                          metadata=meta_new, annotation=item.annotation)
                    subset.append(item_new)
                    counter += 1
                    time += self.length
                    samples_written += buffer

                self.logger().info("# of chunks generated: %d" % len(subset))
                result.extend(subset)

        return flatten_list(result)
