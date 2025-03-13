# from-data

* generates: adc.api.AudioData

Loads the audio files and forwards them as the specified data type.

```
usage: from-data [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [-i [INPUT ...]] [-I [INPUT_LIST ...]] -t
                 {cl,sp}

Loads the audio files and forwards them as the specified data type.

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
                        {TMP} (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the audio files to
                        use; Supported placeholders: {HOME}, {CWD}, {TMP}
                        (default: None)
  -t {cl,sp}, --data_type {cl,sp}
                        The type of data to forward (default: None)
```
