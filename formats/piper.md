## Piper

The Piper format requires a meta-data spreadsheet and a folder with the WAV
files, typically:

* `metadata.csv` - CSV file with text, audio filenames, and speaker names
* `wav/` - directory with audio files

The `metadata.csv` file uses `|` as a delimiter, and has 2 or 3 columns 
depending on if the dataset has a single or multiple speakers. 
There is no header row.

For single speaker datasets:

```
id|text
```

where `id` is the name of the WAV file in the `wav` directory. For example, 
an `id` of `1234` means that `wav/1234.wav` should exist.

For multi-speaker datasets:

```
id|speaker|text
```

where `speaker` is the name of the utterance's speaker. Speaker ids will 
automatically be assigned based on the number of utterances per speaker 
(speaker id 0 has the most utterances).


## Source

https://github.com/rhasspy/piper/blob/master/TRAINING.md#dataset-format
