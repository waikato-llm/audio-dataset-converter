import abc
import argparse
import os
from random import Random

from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from kasperl.api import flatten_list, make_list
from adc.api import AudioData

MIN_RAND = 0
MAX_RAND = 1000


AUG_MODE_REPLACE = "replace"
AUG_MODE_ADD = "add"
AUG_MODES = [
    AUG_MODE_REPLACE,
    AUG_MODE_ADD,
]


class BaseAudioAugmentationFilter(Filter, abc.ABC):
    """
    Ancestor for audio augmentation filters.
    """

    def __init__(self, mode: str = AUG_MODE_REPLACE, suffix: str = None,
                 seed: int = None, seed_augmentation: bool = False, threshold: float = 0.0,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param mode: the augmentation mode to use
        :type mode: str
        :param suffix: the suffix to use for the file names in case of augmentation mode 'add'
        :type suffix: str
        :param seed: the seed value to use for the random number generator; randomly seeded if not provided
        :type seed: int
        :param seed_augmentation: whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value
        :type seed_augmentation: bool
        :param threshold: the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)
        :type threshold: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.mode = mode
        self.suffix = suffix
        self.seed = seed
        self.seed_augmentation = seed_augmentation
        self.threshold = threshold
        self._random = None

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-m", "--mode", choices=AUG_MODES, help="The augmentation mode to use.", default=AUG_MODE_REPLACE, required=False)
        parser.add_argument("--suffix", type=str, help="The suffix to use for the file names in case of augmentation mode %s." % AUG_MODE_ADD, default=None, required=False)
        parser.add_argument("-s", "--seed", type=int, help="The seed value to use for the random number generator; randomly seeded if not provided", default=None, required=False)
        parser.add_argument("-a", "--seed_augmentation", action="store_true", help="Whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from %d to %d for the augmentation." % (MIN_RAND, MAX_RAND), required=False)
        parser.add_argument("-T", "--threshold", type=float, help="the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)", default=0.0, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.mode = ns.mode
        self.suffix = ns.suffix
        self.seed = ns.seed
        self.seed_augmentation = ns.seed_augmentation
        self.threshold = ns.threshold

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.mode is None:
            self.mode = AUG_MODE_REPLACE
        if self.seed_augmentation is None:
            self.seed_augmentation = False
        if self.threshold is None:
            self.threshold = 0.0
        self._random = Random(self.seed)

    @abc.abstractmethod
    def _default_suffix(self) -> str:
        """
        Returns the default suffix to use for audio files when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        raise NotImplementedError()

    def _get_suffix(self) -> str:
        """
        Returns the suffix to use when using imgaug mode "add".

        :return: the suffix to use
        :rtype: str
        """
        if self.suffix is None:
            return self._default_suffix()
        else:
            return self.suffix

    def _can_augment(self) -> bool:
        """
        Checks whether augmentation can take place.

        :return: whether we can augment
        :rtype: bool
        """
        return True

    @abc.abstractmethod
    def _augment(self, item: AudioData, aug_seed: int, audio_name: str) -> AudioData:
        """
        Augments the audio data.

        :param item: the data to augment
        :type item: AudioData
        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :param audio_name: the new audio name
        :type audio_name: str
        :return: the potentially updated audio data
        :rtype: AudioData
        """
        raise NotImplementedError()

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            # cannot augment?
            if not self._can_augment():
                result.append(item)
                continue

            # below threshold?
            if self._random.random() < self.threshold:
                result.append(item)
                continue

            # augment
            if self.seed_augmentation:
                aug_seed = self._random.randint(MIN_RAND, MAX_RAND)
            else:
                aug_seed = None
            audio_name_parts = os.path.splitext(item.audio_name)
            audio_name_new = audio_name_parts[0] + self._get_suffix() + audio_name_parts[1]
            item_new = self._augment(item, aug_seed, audio_name_new)

            if self.mode == AUG_MODE_ADD:
                result.append(item)
                result.append(item_new)
            elif self.mode == AUG_MODE_REPLACE:
                result.append(item_new)
            else:
                raise Exception("Unknown augmentation mode: %s" + self.mode)

        return flatten_list(result)
