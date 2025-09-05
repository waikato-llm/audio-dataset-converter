# from-pyfunc

* generates: adc.api.AudioData

Loads the audio files via the declared function and forwards them as the specified data type. The function must take a string as input and output an iterable of audio containers matching the data type.

```
usage: from-pyfunc [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [-i [INPUT ...]] [-I [INPUT_LIST ...]]
                   [--resume_from RESUME_FROM] -f FUNCTION -t {cl,sp}

Loads the audio files via the declared function and forwards them as the
specified data type. The function must take a string as input and output an
iterable of audio containers matching the data type.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT ...], --input [INPUT ...]
                        Path to the audio file(s) to read; glob syntax is
                        supported; Supported placeholders: {HOME}, {CWD},
                        {TMP}, {INPUT_PATH}, {INPUT_NAMEEXT},
                        {INPUT_NAMENOEXT}, {INPUT_EXT}, {INPUT_PARENT_PATH},
                        {INPUT_PARENT_NAME} (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the audio files to
                        use; Supported placeholders: {HOME}, {CWD}, {TMP},
                        {INPUT_PATH}, {INPUT_NAMEEXT}, {INPUT_NAMENOEXT},
                        {INPUT_EXT}, {INPUT_PARENT_PATH}, {INPUT_PARENT_NAME}
                        (default: None)
  --resume_from RESUME_FROM
                        Glob expression matching the file to resume from,
                        e.g., '*/012345.wav' (default: None)
  -f FUNCTION, --function FUNCTION
                        The Python function to use, format:
                        module_name:function_name (default: None)
  -t {cl,sp}, --data_type {cl,sp}
                        The type of data to forward (default: None)
```
