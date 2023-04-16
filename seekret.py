import os
import sys
import base64
import re
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def usage():
    print("Usage: find_sensitive_info.py [-v|--verbose] [url_list_file]")
    sys.exit(1)


def search_sensitive_info(decoded):
    return sensitive_info_pattern.search(decoded)


def process_file(file):
    with open(file) as f:
        content = f.read()

    for match in base64_pattern.finditer(content):
        encoded = match.group(0)
        try:
            decoded = base64.b64decode(encoded).decode('utf-8')
        except (TypeError, UnicodeDecodeError):
            continue

        sensitive_info = search_sensitive_info(decoded)
        if sensitive_info:
            print(f"{file} (Base64 decoded): {decoded}")

    for match in sensitive_info_pattern.finditer(content):
        print(f"{file}: {match.group(0)}")


def main():
    if len(sys.argv) < 2:
        usage()

    verbose = False
    if sys.argv[1] in ['-v', '--verbose']:
        verbose = True
        sys.argv.pop(1)

    if len(sys.argv) < 2:
        usage()

    url_list_file = sys.argv[1]
    directory = "downloaded_js_files"
    Path(directory).mkdir(parents=True, exist_ok=True)

    with open(url_list_file) as f:
        urls = [line.strip() for line in f.readlines()]

    for url in urls:
        if verbose:
            print(f"Downloading {url}")

        file_name = os.path.basename(url)
        response = requests.get(url)
        with open(os.path.join(directory, file_name), 'wb') as f:
            f.write(response.content)

    # Read regex patterns from file and combine them
    with open('regex_patterns.txt') as f:
        regex_patterns = [pattern.strip() for pattern in f.readlines()]
    combined_regex = "|".join(regex_patterns)

    base64_regex = r"[A-Za-z0-9+/=]{10,}"

    global sensitive_info_pattern, base64_pattern
    sensitive_info_pattern = re.compile(combined_regex)
    base64_pattern = re.compile(base64_regex)

    if verbose:
        print("Searching for sensitive information...")

    js_files = list(Path(directory).rglob("*.js"))

    with ThreadPoolExecutor() as executor:
        executor.map(process_file, js_files)


if __name__ == "__main__":
    main()
