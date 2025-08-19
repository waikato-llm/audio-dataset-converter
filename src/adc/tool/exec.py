import logging
import traceback

from adc.core import ENV_ADC_LOGLEVEL
from adc.registry import available_generators
from adc.tool.convert import main as convert_main, CONVERT
from kasperl.api import perform_pipeline_execution

EXEC = "adc-exec"

_logger = logging.getLogger(EXEC)


def main(args=None):
    """
    The main method for parsing command-line arguments.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    perform_pipeline_execution(ENV_ADC_LOGLEVEL, args, EXEC, None,
                               CONVERT, convert_main, available_generators(), _logger)


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
        return 1


if __name__ == '__main__':
    main()
