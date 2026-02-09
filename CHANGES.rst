Changelog
=========

0.1.1 (????-??-??)
------------------

- `to-commonvoice-sp` writer now creates output directories automatically, can retrieve the client_id from meta-data now
- `from-commonvoice-sp` reader now adds the additional columns from its .tsv file into meta-data
- added `to-piper-sp` writer and `from-piper-sp` reader (https://github.com/rhasspy/piper/blob/master/TRAINING.md#dataset-format)
- added support for speaker companion file to TXT format (classification and speech)
- `AudioData` now implements mixins AnnotationHandler, SourceSupporter, and BytesSupporter


0.1.0 (2025-10-31)
------------------

- `split-records` filter now allows specifying the meta-data field in which to store the split name
- the `tee` meta-filter can now forward or drop the incoming data based on a meta-data evaluation
- the `sub-process` filter can be used for processing data with sub-flow of filters, can be conditional based on meta-data evaluation
- the `metadata-from-name` filter can work on the path now as well (must be present)
- switched to `kasperl` library for base API and generic pipeline plugins
- added `@abc.abstractmethod` decorator where appropriate
- the `adc-exec` tool now uses all remaining parameters as the pipeline components rather than having
  to specify them via the `-p/--pipeline` parameter, making it easy to simply prefix the `adc-exec`
  command to an existing `adc-convert` command-line
- added the `text-file` and `csv-file` generators that work off files to populate the variable(s)
- added support for class lister with ignored classes
- `adc-exec` can load pipelines from file now as well, useful when dealing with large pipelines
- added `--load_pipeline` option to `adc-convert`
- added `from-text-file` reader and `to-text-file` writer
- readers now locate files the first time the `read()` method gets called rather than in the
  `initialized()`, to allow more dynamic placeholders
- added `from-text-file` reader and `to-text-file` writer
- added `block`, `stop` filters for controlling the flow of data (via meta-data conditions)
- added email support with `get-email` reader and `send-email` writer
- added `list-files` reader for listing files in a directory
- added `list-to-sequence` stream filter that forwards list items one by one
- added `console` writer for outputting the data on stdout that is coming through
- added `watch-dir` meta-reader that uses the watchdog library to react to file-system events
  rather than using fixed-interval polling like `poll-dir`
- added `delete-files` writer
- added `copy-files` filter
- added support for caching plugins via `ADC_CLASS_CACHE` environment variable
- added `to-metadata` writer that outputs the meta-data of an image
- added `attach-metadata` filter that loads meta-data from a directory and attaches it to the data passing through
- added `annotation-to-storage` and `annotation-from-storage` filters
- annotation data is now being type-checked when setting it
- requiring seppl>=0.3.0 now


0.0.4 (2025-07-15)
------------------

- requiring seppl>=0.2.20 now for improved help requests in `adc-convert` tool


0.0.3 (2025-07-10)
------------------

- added `set-placeholder` filter for dynamically setting (temporary) placeholders at runtime
- added `--resume_from` option to relevant readers that allows resuming the data processing
  from the first file that matches this glob expression (e.g., `*/012345.wav`)
- requiring seppl>=0.2.17 now for resume, split group, skippable plugin support and avoiding deprecated use of pkg_resources
- `to-adams-sp` writer now uses `-t` short flag for the transcript like the `from-adams-sp` reader
- added the `from-multi` meta-reader that combines multiple base readers and returns their output
- added the `to-multi` meta-writer that forwards the data to multiple base writers
- using `wai_common` instead of `wai.common` now
- added `split_group` parameter to splittable writers (stream/batch)
- fixed the construction of the error messages in the pyfunc reader/filter/writer classes
- added `metadata-to-placeholder` filter to transfer meta-data files into placeholders


0.0.2 (2025-03-14)
------------------

- added `setuptools` as dependency
- switched to underscores in project name
- added `discard-by-name` filter
- requiring seppl>=0.2.13 now
- added support for aliases
- added placeholder support to tools: `adc-convert`, `adc-exec`
- added placeholder support to readers: `from-adams-ac`, `from-subdir-ac`, `from-txt-ac`, `from-adams-sp`,
  `from-commonvoice-sp`, `from-festvox-sp`, `from-hf-audiofolder-sp`, `from-txt-sp`, `from-data`, `poll-dir`,
  `from-pyfunc`
- added placeholder support to writers: `to-adams-ac`, `to-subdir-ac`, `to-txt-ac`, `to-adams-sp`, `to-commonvoice-sp`,
  `to-festvox-sp`, `to-hf-audiofolder-sp`, `to-txt-sp`, `to-audioinfo`, `to-data`


0.0.1 (2024-07-05)
------------------

- initial release

