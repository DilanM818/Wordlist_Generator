# Webpage Word Frequency Counter

This Python script analyzes a webpage and extracts the most frequent words, providing a simple command-line interface for users.  It utilizes libraries like `requests`, `BeautifulSoup`, `re`, and `click` to fetch, parse, and process web content.

## Features

* Fetches the HTML content of a given URL.
* Extracts all words from the HTML, removing HTML tags.
* Counts the occurrences of each word, allowing for a minimum word length filter.
* Displays the top 10 most frequent words (or fewer if the webpage has less).
* Command-line interface using `click` for easy interaction.

## Installation

  **Clone the repository:**
    ```
    git clone https://github.com/DilanM818/Word-Extractor
    ```
## Usage

```bash
python3 wordextractor.py --url <target url> --length <min. length of word>
