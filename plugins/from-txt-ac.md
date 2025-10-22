# from-txt-ac

* generates: adc.api.AudioClassificationData

Loads the audio classification from the associated .txt file.

```
usage: from-txt-ac [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   [-N LOGGER_NAME] [-i [INPUT ...]] [-I [INPUT_LIST ...]]
                   [--resume_from RESUME_FROM] [--rel_path REL_PATH]

Loads the audio classification from the associated .txt file.

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
                        Path to the text file(s) listing the report files to
                        use; Supported placeholders: {HOME}, {CWD}, {TMP}
                        (default: None)
  --resume_from RESUME_FROM
                        Glob expression matching the file to resume from,
                        e.g., '*/012345.txt' (default: None)
  --rel_path REL_PATH   The relative path to the audio files. (default: .)
```
