# from-styletts2-sp

* generates: adc.api.SpeechData

Reads the speech data in StyleTTS2 format (https://github.com/yl4579/StyleTTS2#training).

```
usage: from-styletts2-sp [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                         [-N LOGGER_NAME] [-i [INPUT ...]]
                         [-I [INPUT_LIST ...]] [--resume_from RESUME_FROM]
                         [--speaker_key SPEAKER_KEY] [-r REL_PATH]

Reads the speech data in StyleTTS2 format
(https://github.com/yl4579/StyleTTS2#training).

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -i [INPUT ...], --input [INPUT ...]
                        Path to the metadata text file(s) to read; glob syntax
                        is supported; Supported variables: {HOME}, {CWD},
                        {TMP} (default: None)
  -I [INPUT_LIST ...], --input_list [INPUT_LIST ...]
                        Path to the text file(s) listing the metadata text
                        files to use; Supported variables: {HOME}, {CWD},
                        {TMP} (default: None)
  --resume_from RESUME_FROM
                        Glob expression matching the file to resume from,
                        e.g., '*/012345.txt' (default: None)
  --speaker_key SPEAKER_KEY
                        The key in the meta-data with the speaker name/ID.
                        (default: speaker)
  -r REL_PATH, --rel_path REL_PATH
                        The relative path to the audio files. (default: wav)
```
