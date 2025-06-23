# pitch-shift

* accepts: adc.api.AudioData
* generates: adc.api.AudioClassificationData, adc.api.SpeechData

Augmentation method for shifting the pitch of audio files.

```
usage: pitch-shift [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [--skip] [-m {replace,add}]
                   [--suffix SUFFIX] [-s SEED] [-a] [-T THRESHOLD]
                   [-f FROM_STEPS] [-t TO_STEPS]
                   [--bins_per_octave BINS_PER_OCTAVE]
                   [--resample_type {kaiser_best,kaiser_fast,fft,polyphase,linear,zero_order_hold,sinc_best,sinc_medium,sinc_fastest,soxr_vhq,soxr_hq,soxr_mq,soxr_lq,soxr_qq}]

Augmentation method for shifting the pitch of audio files.

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
  -f FROM_STEPS, --from_steps FROM_STEPS
                        The minimum (fractional) steps to shift. (default:
                        None)
  -t TO_STEPS, --to_steps TO_STEPS
                        The maximum (fractional) steps to shift. (default:
                        None)
  --bins_per_octave BINS_PER_OCTAVE
                        How many steps per octave. (default: 12)
  --resample_type {kaiser_best,kaiser_fast,fft,polyphase,linear,zero_order_hold,sinc_best,sinc_medium,sinc_fastest,soxr_vhq,soxr_hq,soxr_mq,soxr_lq,soxr_qq}
                        The resampling type to apply. (default: kaiser_best)
```
