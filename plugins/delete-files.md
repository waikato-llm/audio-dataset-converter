# delete-files

* accepts: str, list

Deletes the files associate with the file names it receives. Placeholders in the file names get expanded automatically.

```
usage: delete-files [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                    [-N LOGGER_NAME] [--skip]

Deletes the files associate with the file names it receives. Placeholders in
the file names get expanded automatically.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
```
