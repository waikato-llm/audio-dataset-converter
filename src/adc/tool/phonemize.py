import argparse
import logging
import os
import sys
import traceback
from typing import List

from seppl.io import locate_files
from seppl.variables import load_user_defined_variables, variable_list
from wai.logging import init_logging, set_logging_level, add_logging_level

from adc.api import Phonemizer
from adc.core import ENV_ADC_LOGLEVEL
from adc.registry import available_phonemizers

PHONEMIZE = "adc-phonemize"

_logger = logging.getLogger(PHONEMIZE)


def generate_phonemes(text: List[str] = None, paths: List[str] = None, output: str = None,
                      phonemizer: str = None, logger: logging.Logger = None):
    """
    Phonemizes the textual data.

    :param text: the lines of text to process and output on stdout
    :type text: list
    :param paths: the file(s) to phonemize
    :type paths: list
    :param output: the output directory to store the phonemized files in
    :type output: str
    :param phonemizer: the phonemizer command-line to use
    :type phonemizer: str
    :param logger: the optional logger instance to use
    :type logger: logging.Logger
    """
    all_paths = None
    if paths is not None:
        if output is None:
            raise Exception("No output directory specified!")
        all_paths = locate_files(paths, fail_if_empty=True, default_glob="*.txt")
        if len(all_paths) > 1:
            logger.info("Found %d input files" % len(all_paths))

    # initialize the phonemizer
    _phonemizer = Phonemizer.parse_phonemizer(phonemizer, available_phonemizers=available_phonemizers())
    _phonemizer.initialize()

    # just text?
    if text is not None:
        for line in text:
            processed = _phonemizer.phonemize(line)
            print(processed)

    # iterate files?
    if all_paths is not None:
        for path in all_paths:
            if logger is not None:
                logger.info("Processing: %s" % path)
            path_out = os.path.join(output, os.path.basename(path))
            with open(path, "r") as fp:
                lines = fp.readlines()

            lines_out = []
            for line in lines:
                line_out = _phonemizer.phonemize(line)
                lines_out.append(line_out)

            if logger is not None:
                logger.info("Writing: %s" % path_out)
            with open(path_out, "w") as fp:
                fp.write("\n".join(lines_out))

    _phonemizer.finalize()


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    init_logging(env_var=ENV_ADC_LOGLEVEL)
    parser = argparse.ArgumentParser(
        description="Tool for phonemizing text.",
        prog=PHONEMIZE,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--text", metavar="TEXT", help="The text to process, outputs the result to stdout.", default=None, type=str, required=False, nargs="*")
    parser.add_argument("-i", "--input", metavar="FILE", help="The text files to process (requires -o/--output); supports glob syntax. " + variable_list(input_based=False), default=None, type=str, required=False, nargs="*")
    parser.add_argument("-o", "--output", metavar="DIR", help="The directory to store the phonemized text in. " + variable_list(input_based=False), type=str, required=False, default=None)
    parser.add_argument("-p", "--phonemizer", type=str, help="The phonemizer command-line to use.", required=True, default=None)
    parser.add_argument("--variables", "--placeholders", metavar="FILE", dest="variables", help="The file with custom variables to load (format: key=value).", required=False, default=None, type=str)
    add_logging_level(parser)
    parsed = parser.parse_args(args=args)
    set_logging_level(_logger, parsed.logging_level)
    if parsed.variables is not None:
        if not os.path.exists(parsed.variables):
            _logger.error("Variable file not found: %s" % parsed.variables)
        else:
            _logger.info("Loading custom variables from: %s" % parsed.variables)
            load_user_defined_variables(parsed.variables)
    generate_phonemes(text=parsed.text, paths=parsed.input, output=parsed.output,
                      phonemizer=parsed.phonemizer, logger=_logger)


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        traceback.print_exc()
        print("options: %s" % str(sys.argv[1:]), file=sys.stderr)
        return 1


if __name__ == '__main__':
    main()
