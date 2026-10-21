# to-loudness

* accepts: adc.api.AudioData

Determines the loudness or loudness range of the audio clips and saves them to the specified CSV file.

```
usage: to-loudness [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [--skip]
                   [--split_ratios SPLIT_RATIOS [SPLIT_RATIOS ...]]
                   [--split_names SPLIT_NAMES [SPLIT_NAMES ...]]
                   [--split_group SPLIT_GROUP] -o OUTPUT
                   [-t {loudness,loudness-range}]

Determines the loudness or loudness range of the audio clips and saves them to
the specified CSV file.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --split_ratios SPLIT_RATIOS [SPLIT_RATIOS ...]
                        The split ratios to use for generating the splits
                        (must sum up to 100) (default: None)
  --split_names SPLIT_NAMES [SPLIT_NAMES ...]
                        The split names to use for the generated splits.
                        (default: None)
  --split_group SPLIT_GROUP
                        The regular expression with a single group used for
                        keeping items in the same split, e.g., for identifying
                        the base name of a file or the sample ID. (default:
                        None)
  -o OUTPUT, --output OUTPUT
                        The CSV file to store the loudness in. Any defined
                        splits get added above the file. Supported variables:
                        {HOME}, {CWD}, {TMP}, {INPUT_PATH}, {INPUT_NAMEEXT},
                        {INPUT_NAMENOEXT}, {INPUT_EXT}, {INPUT_PARENT_PATH},
                        {INPUT_PARENT_NAME} (default: None)
  -t {loudness,loudness-range}, --output_type {loudness,loudness-range}
                        What to calculate and output. (default: loudness)
```
