# from-festvox-sp

* generates: adc.api.SpeechData

Reads the speech data in Festvox format.

```
usage: from-festvox-sp [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [-i [INPUT [INPUT ...]]]
                       [-I [INPUT_LIST [INPUT_LIST ...]]] [-r REL_PATH]

Reads the speech data in Festvox format.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT [INPUT ...]], --input [INPUT [INPUT ...]]
                        Path to the text file(s) to read; glob syntax is
                        supported (default: None)
  -I [INPUT_LIST [INPUT_LIST ...]], --input_list [INPUT_LIST [INPUT_LIST ...]]
                        Path to the text file(s) listing the text files to use
                        (default: None)
  -r REL_PATH, --rel_path REL_PATH
                        The relative path to the audio files. (default: .)
```
