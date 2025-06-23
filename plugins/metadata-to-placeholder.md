# metadata-to-placeholder

* accepts: seppl.AnyData
* generates: seppl.AnyData

Sets the placeholder with the value from the meta-data passing through.

```
usage: metadata-to-placeholder [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                               [-N LOGGER_NAME] [--skip] [-k METADATA_KEY] -p
                               PLACEHOLDER

Sets the placeholder with the value from the meta-data passing through.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -k METADATA_KEY, --metadata_key METADATA_KEY
                        The key in the meta-data to get the value for the
                        placeholder from. (default: None)
  -p PLACEHOLDER, --placeholder PLACEHOLDER
                        The name of the placeholder, without curly brackets.
                        (default: None)
```
