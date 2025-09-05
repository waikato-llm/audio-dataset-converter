# to-audioinfo

* accepts: adc.api.AudioData

Outputs information about the audio files.

```
usage: to-audioinfo [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip] [-o OUTPUT_FILE] [-f {csv,json}]

Outputs information about the audio files.

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
                        The file to store the audio information in; outputs to
                        stdout if no file provided. Supported placeholders:
                        {HOME}, {CWD}, {TMP}, {INPUT_PATH}, {INPUT_NAMEEXT},
                        {INPUT_NAMENOEXT}, {INPUT_EXT}, {INPUT_PARENT_PATH},
                        {INPUT_PARENT_NAME} (default: None)
  -f {csv,json}, --output_format {csv,json}
                        The format to use for the output. (default: text)
```
