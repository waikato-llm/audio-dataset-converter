# generate-chunks

* accepts: adc.api.AudioData
* generates: adc.api.AudioClassificationData, adc.api.SpeechData

Splits the audio into chunks of the specified length.

```
usage: generate-chunks [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [--skip] [-L LENGTH] [-k METADATA_KEY]

Splits the audio into chunks of the specified length.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -L LENGTH, --length LENGTH
                        The length of the chunks in seconds. (default: 1.0)
  -k METADATA_KEY, --metadata_key METADATA_KEY
                        The key in the meta-data to store the offset under.
                        (default: offset)
```
