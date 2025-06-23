# time-stretch

* accepts: adc.api.AudioData
* generates: adc.api.AudioClassificationData, adc.api.SpeechData

Augmentation method for stretching the time of audio files (speed up/slow down).

```
usage: time-stretch [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip] [-m {replace,add}]
                    [--suffix SUFFIX] [-s SEED] [-a] [-T THRESHOLD]
                    [-f FROM_RATE] [-t TO_RATE]

Augmentation method for stretching the time of audio files (speed up/slow
down).

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -m {replace,add}, --mode {replace,add}
                        The augmentation mode to use. (default: replace)
  --suffix SUFFIX       The suffix to use for the file names in case of
                        augmentation mode add. (default: None)
  -s SEED, --seed SEED  The seed value to use for the random number generator;
                        randomly seeded if not provided (default: None)
  -a, --seed_augmentation
                        Whether to seed the augmentation; if specified, uses
                        the seeded random generator to produce a seed value
                        from 0 to 1000 for the augmentation. (default: False)
  -T THRESHOLD, --threshold THRESHOLD
                        the threshold to use for Random.rand(): if equal or
                        above, augmentation gets applied; range: 0-1; default:
                        0 (= always) (default: 0.0)
  -f FROM_RATE, --from_rate FROM_RATE
                        The minimum stretch factor (<1: slow down, 1: same,
                        >1: speed up). (default: None)
  -t TO_RATE, --to_rate TO_RATE
                        The maximum stretch factor (<1: slow down, 1: same,
                        >1: speed up). (default: None)
```
