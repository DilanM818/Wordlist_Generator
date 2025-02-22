# Web Crawler and Password Mutator

## Description

This Python script is a command-line tool that crawls a website, extracts the most frequent words from its content, and generates common password mutations based on those words. It's designed to help security professionals and researchers understand potential password patterns derived from website content.

**Key Features:**

* **Web Crawling:** Crawls a website to a specified depth, fetching content from multiple pages.
* **Word Extraction:** Extracts all words from the HTML content of web pages, removing HTML tags.
* **Frequency Analysis:** Counts the occurrences of words and identifies the top most frequent words.
* **Password Mutation Generation:** Generates a list of password mutations based on the top words, incorporating common password patterns like capitalization, number and symbol appending, year variations, and seasonal words.
* **Command-Line Interface (CLI):**  Uses `click` to provide a user-friendly command-line interface for easy use and customization.
* **Output Options:** Can output the top words and/or password mutations to files.

## Installation

  **Clone the repository:**
    ```
    git clone https://github.com/DilanM818/Web-Crawler
    ```
## Usage

```bash
python3 webcrawler.py [Options]

Options:
  -u, --url <TEXT>               URL of webpage to extract from  [required]
  -l, --length <INTEGER>         Minimum word length (default: 0, no limit)
  -o, --output <TEXT>            Output file to save results
  -d, --depth <INTEGER>          Crawling depth (default: 0, only searches given URL)
  -m, --mutate                   Generate and output common password mutations.
  -mo, --mutation-output <TEXT>  Output file to save password
  --help                         
```
**Disclaimer:**

**Use this tool responsibly and ethically.**  Password generation based on website content should be used for security research, penetration testing (with proper authorization), and educational purposes.  **Do not use this tool for illegal activities or unauthorized access to systems.**  The generated passwords are based on common patterns and may not be effective against sophisticated password policies.
