# list-files

* generates: builtins.str

Lists files in the specified directory and forwards them.

```
usage: list-files [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] -p DIR [-r REGEXP] [--as_list]

Lists files in the specified directory and forwards them.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -p DIR, --path DIR    The directory to list the files in; Supported
                        placeholders: {HOME}, {CWD}, {TMP}, {INPUT_PATH},
                        {INPUT_NAMEEXT}, {INPUT_NAMENOEXT}, {INPUT_EXT},
                        {INPUT_PARENT_PATH}, {INPUT_PARENT_NAME} (default:
                        None)
  -r REGEXP, --regexp REGEXP
                        The regular expression that the files must match.
                        (default: .*)
  --as_list             Whether to forward the files as a list or one by one.
                        (default: False)
```
