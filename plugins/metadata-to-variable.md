# metadata-to-placeholder

* accepts: seppl.AnyData
* generates: seppl.AnyData
* alias(es): metadata-to-placeholder

Sets the variable with the value from the meta-data passing through.

```
usage: metadata-to-variable [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                            [-N LOGGER_NAME] [--skip] [-k METADATA_KEY] -V
                            VARIABLE

Sets the variable with the value from the meta-data passing through.

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
                        variable from. (default: None)
  -V VARIABLE, -p VARIABLE, --variable VARIABLE, --placeholder VARIABLE
                        The name of the variable, without curly brackets.
                        (default: None)
```
