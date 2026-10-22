# to-phoneme-vocab

* accepts: adc.api.SpeechData

Generates a phoneme vocabulary from the collected phonemes.

```
usage: to-phoneme-vocab [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                        [-N LOGGER_NAME] [--skip] [-o OUTPUT_FILE] [-s]

Generates a phoneme vocabulary from the collected phonemes.

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
                        The JSON file to write the vocabulary to; uses stdout
                        if omitted. Supported variables: {HOME}, {CWD}, {TMP}
                        (default: None)
  -s, --space_separated
                        Whether the phonemes are separated with single-space
                        and words with double-space or treated as single-
                        character. (default: False)
```
