# df-audio-data

Expands the placeholders in the format string using the available audio data.

```
usage: df-audio-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [-N LOGGER_NAME] [-f OUTPUT_FORMAT]

Expands the placeholders in the format string using the available audio data.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -f OUTPUT_FORMAT, --output_format OUTPUT_FORMAT
                        The format to use for the output, available
                        placeholders: data, audio-name, audio-format, sample-
                        rate, duration, has-annotations, annotations (default:
                        data)
```
