# to-merged

* accepts: adc.api.AudioData

Merges the audio and saves it in WAV format. Optionally merges the annotations as well. NB: stores the audio in memory before writing it out to disk when the pipeline finishes up.

```
usage: to-merged [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [--skip] -a AUDIO [-A ANNOTATIONS]
                 [-s SEPARATOR]

Merges the audio and saves it in WAV format. Optionally merges the annotations
as well. NB: stores the audio in memory before writing it out to disk when the
pipeline finishes up.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -a AUDIO, --audio AUDIO
                        The WAV file to store the merged audio in. Supported
                        variables: {HOME}, {CWD}, {TMP} (default: None)
  -A ANNOTATIONS, --annotations ANNOTATIONS
                        The text file to store the merged annotations in.
                        Supported variables: {HOME}, {CWD}, {TMP} (default:
                        None)
  -s SEPARATOR, --separator SEPARATOR
                        The separator to use when merging annotations, use \n
                        and \t for newline and separator. (default: )
```
