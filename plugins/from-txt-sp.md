# from-txt-sp

* generates: adc.api.SpeechData

Loads the transcript from the associated .txt file.

```
usage: from-txt-sp [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [-i [INPUT ...]] [-I [INPUT_LIST ...]]
                   [--rel_path REL_PATH]

Loads the transcript from the associated .txt file.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT ...], --input [INPUT ...]
                        Path to the .txt file(s) to read; glob syntax is
                        supported; Supported placeholders: {HOME}, {CWD},
                        {TMP} (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the .txt files to
                        use; Supported placeholders: {HOME}, {CWD}, {TMP}
                        (default: None)
  --rel_path REL_PATH   The relative path to the audio files. (default: .)
```
