# IMPLANT

Wrapper around magic-wormhole.

## Usage

### Receiving side

```bash
uvx --from git+https://github.com/44/implant implant
```

This will show a code like `7-abcde-fghij`, wait for the sender to respond.
Sender is expected to send a folder. Payload is
extracted into temporary directory and is expected to contain `install.py`
self-contained script which is executed using `uv`.

### Sending side

Prepare folder with files to send, including `install.py` script. Then run:

```bash
uvx --from git+https://github.com/44/implant implant --send /path/to/folder --code 7-abcde-fghij
```
