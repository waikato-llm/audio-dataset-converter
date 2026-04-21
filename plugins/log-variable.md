# log-placeholder

* accepts: seppl.AnyData
* generates: seppl.AnyData
* alias(es): log-placeholder

Outputs the values of the specified variables. Logging must be set to INFO for the output to show.

```
usage: log-variable [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip] -V VARIABLE [VARIABLE ...]

Outputs the values of the specified variables. Logging must be set to INFO for
the output to show.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -V VARIABLE [VARIABLE ...], -p VARIABLE [VARIABLE ...], --variable VARIABLE [VARIABLE ...], --placeholder VARIABLE [VARIABLE ...]
                        The name of the variables, without curly brackets.
                        (default: None)
```
