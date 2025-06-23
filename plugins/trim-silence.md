# trim-silence

* accepts: adc.api.AudioData
* generates: adc.api.AudioClassificationData, adc.api.SpeechData

Trims silence from audio files.

```
usage: trim-silence [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip] [--top_db TOP_DB]
                    [--frame_length FRAME_LENGTH] [--hop_length HOP_LENGTH]

Trims silence from audio files.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --top_db TOP_DB       The threshold (in decibels) below reference to
                        consider as silence. (default: 60)
  --frame_length FRAME_LENGTH
                        The number of samples per analysis frame. (default:
                        2048)
  --hop_length HOP_LENGTH
                        The number of samples between analysis frames.
                        (default: 512)
```
