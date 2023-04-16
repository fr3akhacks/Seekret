import os
import sys
import base64
import binascii
import re
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit

def usage():
    print("Usage: find_sensitive_info.py [-v|--verbose] [url_list_file]")
    sys.exit(1)

def search_sensitive_info(decoded):
    return sensitive_info_pattern.search(decoded)

def process_file(file):
    results = []
    with open(file) as f:
        content = f.read()

    for match in base64_pattern.finditer(content):
        encoded = match.group(0)
        
        # Add padding if necessary
        padding = len(encoded) % 4
        if padding:
            encoded += "=" * (4 - padding)

        try:
            decoded = binascii.a2b_base64(encoded).decode('utf-8')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            continue

        sensitive_info = search_sensitive_info(decoded)
        if sensitive_info:
            result = f"{file}: {sensitive_info.group(0)} (Base64 decoded)"
            results.append(result)

    for match in sensitive_info_pattern.finditer(content):
        if match:
            result = f"{file}: {match.group(0)}"
            results.append(result)

    return results

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
        parsed_url = urlsplit(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            print(f"Skipping invalid URL: {url}")
            continue

        if verbose:
            print(f"Downloading {url}")

        file_name = os.path.basename(url)
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            continue

        with open(os.path.join(directory, file_name), 'wb') as f:
            f.write(response.content)

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

    all_results = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_file, js_files)
        for file_results in results:
            all_results.extend(file_results)

    if all_results:
        output_file = "sensitive_info_output.txt"
        with open(output_file, "w") as f:
            for result in all_results:
                print(result)
                f.write(result + "\n")
    else:
        print("No sensitive information found")

if __name__ == "__main__":
    main()
