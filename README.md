Python-HTTP-header-response-checker
===================================

Check HTTP response status codes for URLs listed in a text file. This is a Python 3 rewrite of the original bash header response checker, using the [Requests](https://requests.readthedocs.io/) library.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Add URLs to `pages.txt` (one per line), then run:

```bash
python3 reponse-check.py
```

Use `-i` / `--interactive` to prompt for file paths and domain replacement values, like the original script:

```bash
python3 reponse-check.py -i
```

### Options

| Option | Description |
|--------|-------------|
| `-f`, `--file` | Input file with URLs (default: `pages.txt`) |
| `-o`, `--output` | Results file (default: `results.txt`) |
| `--replace` | URL prefix to replace in each line |
| `--new-url` | Replacement value for `--replace` |
| `--timeout` | Request timeout in seconds (default: 15) |
| `-j`, `--workers` | Concurrent workers (default: 10) |
| `-i`, `--interactive` | Prompt for settings interactively |

### Output format

Each result line is tab-separated:

```
<status_code>	<requested_url>	<final_url_if_redirected>
```

Request failures are written as:

```
ERR	<requested_url>	<error_message>
```

Lines starting with `#` in the input file are ignored.
