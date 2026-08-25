import abc
import argparse
import logging
from typing import Dict, List

from seppl import Plugin, PluginWithLogging, Initializable, split_cmdline, split_args, args_to_objects
from wai.logging import LOGGING_WARNING
from ._data import AudioData


class Watermarker(PluginWithLogging, Initializable, abc.ABC):

    def __init__(self, enabled: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the watermarker.

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
        parser.add_argument("--disable", action="store_true", help="Whether to disable the watermarker")
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

    def _can_watermark(self, data: AudioData) -> bool:
        """
        Checks whether the audio data can be watermarked.

        :param data: the audio data to check
        :type data: AudioData
        :return: True if it can be processed
        :rtype: bool
        """
        return self.enabled

    def _do_watermark(self, data: AudioData) -> AudioData:
        """
        Applies the watermarker algorithm to the supplied audio data.

        :param data: the audio data to process
        :type data: AudioData
        :return: the processed audio data
        :rtype: str
        """
        raise NotImplementedError()

    def watermark(self, data: AudioData) -> AudioData:
        """
        Applies the watermarker algorithm to the supplied audio data.

        :param data: the audio data to process
        :type data: AudioData
        :return: the processed audio data
        :rtype: AudioData
        """
        if self._can_watermark(data):
            if self.logger().isEnabledFor(logging.INFO):
                self.logger().info("Input: %s" % data.audio_name)

            # watermark
            result = self._do_watermark(data)
        else:
            if self.logger().isEnabledFor(logging.INFO):
                self.logger().info("Cannot embed watermark: %s" % data.audio_name)
            result = data

        return result

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        self.logger().info("Finalizing...")

    @classmethod
    def parse_watermarker(cls, cmdline: str, available_watermarkers: Dict[str, Plugin]) -> 'Watermarker':
        """
        Parses the commandline and returns the watermarker plugin.

        :param cmdline: the command-line to parse
        :type cmdline: str
        :param available_watermarkers: the watermarkers to use for parsing
        :type available_watermarkers: dict
        :return: the watermarker plugin
        :rtype: Watermarker
        """
        result = cls.parse_watermarkers(cmdline, available_watermarkers)
        if len(result) != 1:
            raise Exception("Expected a single watermarker, but got: %d" % len(result))
        return result[0]

    @classmethod
    def parse_watermarkers(cls, cmdline: str, available_watermarkers: Dict[str, Plugin]) -> List['Watermarker']:
        """
        Parses the commandline and returns the list of watermarker plugins.

        :param cmdline: the command-line to parse
        :type cmdline: str
        :param available_watermarkers: the watermarkers to use for parsing
        :type available_watermarkers: dict
        :return: the list of watermarker plugins
        :rtype: list
        """
        watermarker_args = split_args(split_cmdline(cmdline), list(available_watermarkers.keys()))
        return args_to_objects(watermarker_args, available_watermarkers)


class WatermarkDetector(PluginWithLogging, Initializable, abc.ABC):

    def __init__(self, enabled: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the watermark detector.

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
        parser.add_argument("--disable", action="store_true", help="Whether to disable the watermark detector")
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

    def _can_detect(self, data: AudioData) -> bool:
        """
        Checks whether the watermark detection can be performed.

        :param data: the audio data to check
        :type data: AudioData
        :return: True if it can be processed
        :rtype: bool
        """
        return self.enabled

    def _do_detect(self, data: AudioData) -> AudioData:
        """
        Applies the watermark detection algorithm to the supplied audio data.

        :param data: the audio data to process
        :type data: AudioData
        :return: the processed audio data
        :rtype: str
        """
        raise NotImplementedError()

    def watermark(self, data: AudioData) -> AudioData:
        """
        Applies the watermarker algorithm to the supplied audio data.

        :param data: the audio data to process
        :type data: AudioData
        :return: the processed audio data
        :rtype: AudioData
        """
        if self._can_detect(data):
            if self.logger().isEnabledFor(logging.INFO):
                self.logger().info("Input: %s" % data.audio_name)

            # watermark
            result = self._do_detect(data)
        else:
            if self.logger().isEnabledFor(logging.INFO):
                self.logger().info("Cannot detect watermark: %s" % data.audio_name)
            result = data

        return result

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        self.logger().info("Finalizing...")

    @classmethod
    def parse_watermark_detector(cls, cmdline: str, available_watermark_detectors: Dict[str, Plugin]) -> 'WatermarkDetector':
        """
        Parses the commandline and returns the watermark detector plugin.

        :param cmdline: the command-line to parse
        :type cmdline: str
        :param available_watermark_detectors: the watermark detectors to use for parsing
        :type available_watermark_detectors: dict
        :return: the watermark detector plugin
        :rtype: WatermarkDetector
        """
        result = cls.parse_watermark_detectors(cmdline, available_watermark_detectors)
        if len(result) != 1:
            raise Exception("Expected a single watermark detector, but got: %d" % len(result))
        return result[0]

    @classmethod
    def parse_watermark_detectors(cls, cmdline: str, available_watermark_detectors: Dict[str, Plugin]) -> List['WatermarkDetector']:
        """
        Parses the commandline and returns the list of watermark detector plugins.

        :param cmdline: the command-line to parse
        :type cmdline: str
        :param available_watermark_detectors: the watermark detectors to use for parsing
        :type available_watermark_detectors: dict
        :return: the list of watermark detector plugins
        :rtype: list
        """
        detector_args = split_args(split_cmdline(cmdline), list(available_watermark_detectors.keys()))
        return args_to_objects(detector_args, available_watermark_detectors)
