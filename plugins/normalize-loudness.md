# normalize-loudness

* accepts: adc.api.AudioData
* generates: adc.api.AudioClassificationData, adc.api.SpeechData

Normalizes the audio to the specified target LUFS (loudness units full scale). Audio gets automatically converted to mono.

```
usage: normalize-loudness [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                          [-N LOGGER_NAME] [--skip] [-t TARGET_LUFS]
                          [-m MAX_PEAK_DBFS]

Normalizes the audio to the specified target LUFS (loudness units full scale).
Audio gets automatically converted to mono.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -t TARGET_LUFS, --target_lufs TARGET_LUFS
                        The target LUFS to use. (default: -23.0)
  -m MAX_PEAK_DBFS, --max_peak_dbfs MAX_PEAK_DBFS
                        The maximum peak dBFS to allow. (default: -1.0)
```
