import logging

import seppl


ENV_ADC_LOGLEVEL = "ADC_LOGLEVEL"
""" environment variable for the global default logging level. """


class Session(seppl.Session):
    """
    Session object shared among reader, filter(s), writer.
    """
    logger: logging.Logger = logging.getLogger("audio-dataset-converter")
    """ the global logger. """
