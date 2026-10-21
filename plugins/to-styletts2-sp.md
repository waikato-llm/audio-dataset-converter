# to-styletts2-sp

* accepts: adc.api.SpeechData

Saves the speech data in StyleTTS2 format (https://github.com/yl4579/StyleTTS2#training). If no speaker key is specified, assumes the data to be single-speaker and uses 0 as speaker ID.

```
usage: to-styletts2-sp [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                       [-N LOGGER_NAME] [--skip]
                       [--split_ratios SPLIT_RATIOS [SPLIT_RATIOS ...]]
                       [--split_names SPLIT_NAMES [SPLIT_NAMES ...]]
                       [--split_group SPLIT_GROUP] -o OUTPUT
                       [--metadata METADATA] [--speaker_key SPEAKER_KEY]
                       [--rel_path REL_PATH] [--annotations_only]

Saves the speech data in StyleTTS2 format
(https://github.com/yl4579/StyleTTS2#training). If no speaker key is
specified, assumes the data to be single-speaker and uses 0 as speaker ID.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  --split_ratios SPLIT_RATIOS [SPLIT_RATIOS ...]
                        The split ratios to use for generating the splits
                        (must sum up to 100) (default: None)
  --split_names SPLIT_NAMES [SPLIT_NAMES ...]
                        The split names to use for the generated splits.
                        (default: None)
  --split_group SPLIT_GROUP
                        The regular expression with a single group used for
                        keeping items in the same split, e.g., for identifying
                        the base name of a file or the sample ID. (default:
                        None)
  -o OUTPUT, --output OUTPUT
                        The directory to store the audio/metadata files in.
                        Any defined splits get added beneath there. Supported
                        variables: {HOME}, {CWD}, {TMP}, {INPUT_PATH},
                        {INPUT_NAMEEXT}, {INPUT_NAMENOEXT}, {INPUT_EXT},
                        {INPUT_PARENT_PATH}, {INPUT_PARENT_NAME} (default:
                        None)
  --metadata METADATA   The name of the meta-data text file. (default:
                        list.txt)
  --speaker_key SPEAKER_KEY
                        The key in the meta-data with the speaker name/ID;
                        assumes single-speaker data if not supplied, i.e.,
                        used 0 as ID. (default: None)
  --rel_path REL_PATH   The relative path to the audio files. (default: wav)
  --annotations_only    Outputs only the annotations. (default: False)
```
