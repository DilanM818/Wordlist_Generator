# Web Wordlist Generator and Password Mutator

**Warning: This script is intended for educational and ethical security testing purposes ONLY. Misuse for unauthorized activities is illegal and unethical. The author is not responsible for any misuse.**

This Python script is a command-line tool that crawls a website, extracts the most frequent words from its content, and optionally generates common password mutations based on those words. It is designed to aid in security assessments and password cracking exercises (for ethical purposes only, such as penetration testing with explicit permission).

## Features

*   **Web Crawling:** Crawls a website starting from a given URL, up to a specified depth, following links to discover more pages.
*   **Word Extraction:** Extracts all words from the HTML content of crawled web pages, discarding HTML tags and focusing on text content.
*   **Word Frequency Analysis:** Counts the occurrences of words and identifies the most frequent words on the website.
*   **Minimum Word Length Filtering:** Allows you to specify a minimum length for words to be considered in the frequency analysis.
*   **Password Mutation Generation:** Generates common password mutations based on the top words, including capitalization, appending years, symbols, numbers, and seasonal words.
*   **Output to File:**  Saves the list of top words and/or generated password mutations to separate output files.
*   **Command-Line Interface:** Uses `click` for a user-friendly command-line interface with options for URL, depth, minimum word length, output files, and mutation generation.

## Usage

### Prerequisites

*   **Python 3.x:**  Ensure you have Python 3 installed on your system.
*   **Required Python Libraries:** Install the necessary libraries using pip:

    ```bash
    pip install requests beautifulsoup4 click
    ```

### Running the Script

1.  **Clone the repository (or download the script):**

    ```bash
    git clone [repository URL] # Replace [repository URL] with the actual repository URL if you have one.
    cd [repository directory]   # Navigate to the directory where the script is located.
    ```

2.  **Make the script executable (if necessary on Linux/macOS):**

    ```bash
    chmod +x wordlist_generator.py
    ```

3.  **Run the script with options:**

    ```bash
    ./wordlist_generator.py [OPTIONS]
    ```

    You will be prompted for the Web URL if you don't provide it as an option.

### Options

The script supports the following command-line options:
```
Options:
  -u, --url <TEXT>               URL of webpage to extract from  [required]
  -l, --length <INTEGER>         Minimum word length (default: 0, no limit)
  -o, --output <TEXT>            Output file to save results
  -d, --depth <INTEGER>          Crawling depth (default: 0, only searches given URL)
  -m, --mutate                   Generate and output common password mutations
  -mo, --mutation-output <TEXT>  Output file to save password mutations
  --help
```

### Examples

*   **Run the script and get top words from a URL, prompting for the URL:**

    ```bash
    ./wordlist_generator.py
    ```

*   **Run the script, specify the URL and minimum word length, and output top words to a file:**

    ```bash
    ./wordlist_generator.py -u http://example.com -l 5 -o top_words.txt
    ```

*   **Run the script with crawling depth 1 and generate password mutations for top words, saving both top words and mutations to separate files:**

    ```bash
    ./wordlist_generator.py -u http://example.com -d 1 -m -o top_words.txt -mo mutations.txt
    ```

## Ethical Use and Disclaimer

**IMPORTANT:** This script is intended for legitimate security testing and educational purposes only. Using this script to access or attempt to gain unauthorized access to systems or information is illegal and unethical.

*   **Use with Permission:** Only use this script on websites you own or have explicit permission to test.
*   **Ethical Considerations:** Be mindful of the ethical implications of password cracking and security testing.
*   **No Guarantee of Success:** This script generates potential password candidates based on website content. There is no guarantee that these mutations will successfully crack any passwords.

**The author is not responsible for any misuse of this script. By using this script, you agree to use it responsibly and ethically, and you acknowledge the potential legal and ethical consequences of misuse.**
