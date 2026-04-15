# log-placeholder

* accepts: seppl.AnyData
* generates: seppl.AnyData

Outputs the values of the specified placeholders. Logging must be set to INFO for the output to show.

```
usage: log-placeholder [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [--skip] -p PLACEHOLDER
                       [PLACEHOLDER ...]

Outputs the values of the specified placeholders. Logging must be set to INFO
for the output to show.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -p PLACEHOLDER [PLACEHOLDER ...], --placeholder PLACEHOLDER [PLACEHOLDER ...]
                        The name of the placeholders, without curly brackets.
                        (default: None)
```
