# Seekret

Seekret is a tool designed to search for sensitive information in JavaScript files by downloading them from the provided URLs and analyzing their contents. The tool can also decode potential Base64 encoded strings and identify sensitive information in them.

## Features
Downloads JavaScript files from a list of URLs
Searches for sensitive information such as API keys, passwords, email addresses, and more
Decodes Base64 encoded strings and searches for sensitive information
Supports parallel processing for faster execution
Verbose mode for additional output
## Prerequisites
Python 3.6 or higher
## Installation
Clone the repository or download the source code.

``git clone https://github.com/your-repo-url/Seekret.git``
Change to the Seekret directory:

``cd Seekret``
## Usage
### Basic usage
Run Seekret by providing a text file containing the URLs of the JavaScript files to be analyzed:


``
python find_sensitive_info.py urls.txt
``
The downloaded JavaScript files will be stored in the downloaded_js_files directory.

### Verbose mode
To enable verbose mode, which provides additional output on the files being downloaded and the search progress, pass the -v or --verbose flag:

``
python find_sensitive_info.py -v urls.txt
``
### Customizing regex patterns
By default, Seekret searches for several common patterns of sensitive information. You can modify the regex patterns in the regex_patterns.txt file to better suit your needs. Each pattern should be placed on a separate line.

## Important Note
Seekret is designed to help identify potential leaks of sensitive information. It might generate false positives or negatives. It's important to review the results and adjust the regex patterns according to your specific requirements.

## License
Seekret is released under the MIT License. See the LICENSE file for details.
