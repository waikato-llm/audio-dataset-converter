# to-pyfunc

* accepts: adc.api.AudioData

Processes the images of the specified data type via the declared Python function. The function must take an audio container as input (matching the data type class) and an optional 'split' string parameter.

```
usage: to-pyfunc [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [-r SPLIT_RATIOS [SPLIT_RATIOS ...]]
                 [-n SPLIT_NAMES [SPLIT_NAMES ...]] -f FUNCTION -t {cl,sp}

Processes the images of the specified data type via the declared Python
function. The function must take an audio container as input (matching the
data type class) and an optional 'split' string parameter.

optional arguments:
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
  -f FUNCTION, --function FUNCTION
                        The Python function to use, format:
                        module_name:function_name (default: None)
  -t {cl,sp}, --data_type {cl,sp}
                        The type of data to forward (default: None)
```
