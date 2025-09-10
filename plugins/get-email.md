# get-email

* generates: builtins.str

Retrieves emails from the specified IMAP folder, saves the attachments in the specified folder and forwards the file names of the saved attachments as list.

```
usage: get-email [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [-d FILE] [-f FOLDER] [-u] [-R] [-r REGEXP]
                 -o DIR [-w POLL_WAIT] [-F PLACEHOLDER] [-S PLACEHOLDER]

Retrieves emails from the specified IMAP folder, saves the attachments in the
specified folder and forwards the file names of the saved attachments as list.

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  -d FILE, --dotenv_path FILE
                        The .env file to load the IMAP environment variables
                        form (IMAP_HOST|IMAP_PORT|IMAP_USER|IMAP_PW); tries to
                        load .env from the current directory if not specified;
                        Supported placeholders: {HOME}, {CWD}, {TMP},
                        {INPUT_PATH}, {INPUT_NAMEEXT}, {INPUT_NAMENOEXT},
                        {INPUT_EXT}, {INPUT_PARENT_PATH}, {INPUT_PARENT_NAME}
                        (default: None)
  -f FOLDER, --folder FOLDER
                        The IMAP folder to obtain emails from. (default:
                        INBOX)
  -u, --only_unseen     Whether to only retrieve unseen/new emails. (default:
                        False)
  -R, --mark_as_read    Whether to mark the emails as read after retrieval.
                        (default: False)
  -r REGEXP, --regexp REGEXP
                        The regular expression that the attachment file names
                        must match. (default: None)
  -o DIR, --output_dir DIR
                        The directory to store the attachments in; Supported
                        placeholders: {HOME}, {CWD}, {TMP}, {INPUT_PATH},
                        {INPUT_NAMEEXT}, {INPUT_NAMENOEXT}, {INPUT_EXT},
                        {INPUT_PARENT_PATH}, {INPUT_PARENT_NAME} (default:
                        None)
  -w POLL_WAIT, --poll_wait POLL_WAIT
                        The poll interval in seconds (default: 60.0)
  -F PLACEHOLDER, --from_placeholder PLACEHOLDER
                        The optional placeholder name to store the FROM email
                        address under, without curly brackets. (default: None)
  -S PLACEHOLDER, --subject_placeholder PLACEHOLDER
                        The optional placeholder name to store the SUBJECT
                        under, without curly brackets. (default: None)
```
