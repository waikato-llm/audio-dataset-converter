# normalize-peak

* accepts: adc.api.AudioData
* generates: adc.api.AudioClassificationData, adc.api.SpeechData

Normalizes the peak to the specified maximum. Audio gets automatically converted to mono.

```
usage: normalize-peak [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                      [-N LOGGER_NAME] [--skip] [-t TARGET_DBFS]

Normalizes the peak to the specified maximum. Audio gets automatically
converted to mono.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -t TARGET_DBFS, --target_dbfs TARGET_DBFS
                        The target dBFS to use. (default: -3.0)
```
