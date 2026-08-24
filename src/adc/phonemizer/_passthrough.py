from adc.api import Phonemizer
from wai.logging import LOGGING_WARNING


class PassThrough(Phonemizer):
    """
    Dummy, just passes through the text, generates no phonemes.
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the phonemizer.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "ph-passthrough"

    def description(self) -> str:
        """
        Returns a description of the phonemizer.

        :return: the description
        :rtype: str
        """
        return "Dummy, just passes through the text, generates no phonemes."

    def _do_phonemize(self, text: str) -> str:
        """
        Applies the phonemizer algorithm to the supplied string.

        :param text: the string to process
        :type text: str
        :return: the processed string
        :rtype: str
        """
        return text
