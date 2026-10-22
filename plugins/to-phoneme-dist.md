# to-phoneme-dist

* accepts: adc.api.SpeechData

Records the phoneme distribution and saves the statistics to the specified file.

```
usage: to-phoneme-dist [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [--skip] [-o OUTPUT_FILE]
                       [-f {text,csv,json}] [-t {counts,percentages}] [-s]

Records the phoneme distribution and saves the statistics to the specified
file.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        The file to write the statistics to; uses stdout if
                        omitted. Supported variables: {HOME}, {CWD}, {TMP}
                        (default: None)
  -f {text,csv,json}, --output_format {text,csv,json}
                        The format to use for the output. (default: text)
  -t {counts,percentages}, --output_type {counts,percentages}
                        How to output the distribution. (default: counts)
  -s, --space_separated
                        Whether the phonemes are separated with single-space
                        and words with double-space or treated as single-
                        character. (default: False)
```
