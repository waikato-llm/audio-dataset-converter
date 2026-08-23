# watermark

* accepts: adc.api.AudioData
* generates: adc.api.AudioData

Applies the specified watermarker plugin to the audio data.

```
usage: watermark [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [--skip] [-p WATERMARKER]

Applies the specified watermarker plugin to the audio data.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -p WATERMARKER, --watermarker WATERMARKER
                        The watermarker command to use. (default: wm-
                        passthrough)
```
