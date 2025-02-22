#!/usr/bin/env python3

import requests  # For making HTTP requests to fetch web pages
import re        # For regular expressions (used for word extraction)
import click     # For creating command-line interfaces
from bs4 import BeautifulSoup  # For parsing HTML content

# Function to fetch the HTML content of a given URL
def get_html_of(url):
    """Fetches the HTML content of a URL.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content as a string.
        Exits with an error if the HTTP status code is not 200.
    """
    resp = requests.get(url)  # Make the HTTP request

    if resp.status_code != 200:  # Check for HTTP errors
        print(f'HTTP status code {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)  # Exit the program with an error code

    return resp.content.decode()  # Decode the response content 

# Function to extract all words from the HTML content
def get_all_words_from(url):
    """Extracts all words from the HTML content of a URL.

    Args:
        url: The URL to extract words from.

    Returns:
        A list of words.
    """
    html = get_html_of(url)  # Get the HTML content
    soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML
    raw_text = soup.get_text()  # Get the text content, removing HTML tags
    return re.findall(r'\w+', raw_text)  # Find all words using a regular expression

# Function to count the occurrences of words in a list
def count_occurrences_in(word_list, min_length):
    """Counts the occurrences of words in a list, considering a minimum length.

    Args:
        word_list: A list of words.
        min_length: The minimum length of a word to be counted.

    Returns:
        A dictionary where keys are words and values are their counts.
    """
    word_count = {}  # Initialize an empty dictionary to store word counts

    for word in word_list:  # Iterate through each word in the list
        if len(word) < min_length:  # Skip words shorter than min_length
            continue
        word_count[word] = word_count.get(word, 0) + 1  # Efficiently count occurrences
        # word_count.get(word, 0) gets the current count of the word (or 0 if it's not in the dictionary yet)
        # + 1 increments the count
        # word_count[word] = ... updates the dictionary with the new count

    return word_count  # Return the dictionary of word counts

# Function to get the top words and their counts
def get_top_words_from(all_words, min_length):
    """Gets the top words and their counts from a list of words.

    Args:
        all_words: A list of all words.
        min_length: The minimum word length.

    Returns:
        A sorted list of tuples, where each tuple contains a word and its count.
        The list is sorted in descending order of counts.
    """
    occurrences = count_occurrences_in(all_words, min_length)  # Count word occurrences
    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)  # Sort by count (descending)


# Click command-line interface setup
@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit)')

def main(url, length):
    """Main function to process the URL and print the top words.

    Args:
        url: The URL of the webpage.
        length: The minimum word length.
    """
    the_words = get_all_words_from(url)  # Extract all words from the URL
    top_words = get_top_words_from(the_words, length)  # Get the top words

    num_words_to_print = min(10, len(top_words))  # Print up to 10 words (or fewer if available)
    for i in range(num_words_to_print):
        print(top_words[i][0])  # Print the word (the 0th element of the tuple)


if __name__ == '__main__':
    main()  # Run the main function if the script is executed
