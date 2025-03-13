# to-subdir-ac

* accepts: adc.api.AudioClassificationData

Saves audio files to sub-directories, using the classification label for the sub-directory.

```
usage: to-subdir-ac [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [-r SPLIT_RATIOS [SPLIT_RATIOS ...]]
                    [-n SPLIT_NAMES [SPLIT_NAMES ...]] -o OUTPUT

Saves audio files to sub-directories, using the classification label for the
sub-directory.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -r SPLIT_RATIOS [SPLIT_RATIOS ...], --split_ratios SPLIT_RATIOS [SPLIT_RATIOS ...]
                        The split ratios to use for generating the splits
                        (must sum up to 100) (default: None)
  -n SPLIT_NAMES [SPLIT_NAMES ...], --split_names SPLIT_NAMES [SPLIT_NAMES ...]
                        The split names to use for the generated splits.
                        (default: None)
  -o OUTPUT, --output OUTPUT
                        The directory to create the sub-directories in
                        according to the classification labels. Any defined
                        splits get added beneath there. Supported
                        placeholders: {INPUT_PATH}, {INPUT_NAMEEXT},
                        {INPUT_NAMENOEXT}, {INPUT_EXT}, {INPUT_PARENT_PATH},
                        {INPUT_PARENT_NAME} (default: None)
```
