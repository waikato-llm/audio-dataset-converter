# from-subdir-ac

* generates: adc.api.AudioClassificationData

Loads audio files from sub-directories, uses the name of the sub-directory as classification label.

```
usage: from-subdir-ac [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                      [-N LOGGER_NAME] [-i [INPUT ...]] [-I [INPUT_LIST ...]]

Loads audio files from sub-directories, uses the name of the sub-directory as
classification label.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT ...], --input [INPUT ...]
                        Path to the directory with the sub-directories
                        containing the audio files; Supported placeholders:
                        {HOME}, {CWD}, {TMP} (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the directories to
                        use; Supported placeholders: {HOME}, {CWD}, {TMP}
                        (default: None)
```
