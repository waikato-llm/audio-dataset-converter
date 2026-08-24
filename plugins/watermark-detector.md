# watermark-detector

* accepts: adc.api.AudioData
* generates: adc.api.AudioData

Applies the specified watermark detector plugin to the audio data.

```
usage: watermark-detector [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                          [-N LOGGER_NAME] [--skip] [-p WATERMARK_DETECTOR]

Applies the specified watermark detector plugin to the audio data.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -p WATERMARK_DETECTOR, --watermark_detector WATERMARK_DETECTOR
                        The watermark detector command to use. (default: wmd-
                        passthrough)
```
