# resample

* accepts: adc.api.AudioData
* generates: adc.api.AudioClassificationData, adc.api.SpeechData

Resamples the audio data with the supplied sample rate.

```
usage: resample [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-N LOGGER_NAME]
                [--skip] [-s SAMPLE_RATE]
                [-t {kaiser_best,kaiser_fast,fft,polyphase,linear,zero_order_hold,sinc_best,sinc_medium,sinc_fastest,soxr_vhq,soxr_hq,soxr_mq,soxr_lq,soxr_qq}]

Resamples the audio data with the supplied sample rate.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -s SAMPLE_RATE, --sample_rate SAMPLE_RATE
                        The sample rate to use for the audio. (default: 22050)
  -t {kaiser_best,kaiser_fast,fft,polyphase,linear,zero_order_hold,sinc_best,sinc_medium,sinc_fastest,soxr_vhq,soxr_hq,soxr_mq,soxr_lq,soxr_qq}, --resample_type {kaiser_best,kaiser_fast,fft,polyphase,linear,zero_order_hold,sinc_best,sinc_medium,sinc_fastest,soxr_vhq,soxr_hq,soxr_mq,soxr_lq,soxr_qq}
                        The resampling type to apply. (default: kaiser_best)
```
