# send-email

* accepts: seppl.AnyData

Attaches the incoming file(s) and sends them to the specified email address(es).

```
usage: send-email [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                  [-N LOGGER_NAME] [--skip] [-d FILE] -f EMAIL -t EMAIL
                  [EMAIL ...] [-s SUBJECT] [-b TEXT]

Attaches the incoming file(s) and sends them to the specified email
address(es).

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --skip                Disables the plugin, removing it from the pipeline.
                        (default: False)
  -d FILE, --dotenv_path FILE
                        The .env file to load the SMTP environment variables
                        form
                        (SMTP_HOST|SMTP_PORT|SMTP_STARTTLS|SMTP_USER|SMTP_PW);
                        tries to load .env from the current directory if not
                        specified; Supported placeholders: {HOME}, {CWD},
                        {TMP}, {INPUT_PATH}, {INPUT_NAMEEXT},
                        {INPUT_NAMENOEXT}, {INPUT_EXT}, {INPUT_PARENT_PATH},
                        {INPUT_PARENT_NAME} (default: None)
  -f EMAIL, --email_from EMAIL
                        The email address to use for FROM. (default: None)
  -t EMAIL [EMAIL ...], --email_to EMAIL [EMAIL ...]
                        The email address(es) to send the email TO. (default:
                        None)
  -s SUBJECT, --subject SUBJECT
                        The SUBJECT for the email. (default: None)
  -b TEXT, --body TEXT  The email body to use. (default: None)
```
