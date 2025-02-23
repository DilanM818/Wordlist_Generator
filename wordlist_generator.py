#!/usr/bin/env python3

from bs4 import BeautifulSoup  # For parsing HTML content (for easy HTML manipulation)
import click     # For creating command-line interfaces
import datetime # For getting the current year for password mutations
import re      # For regular expressions (used for word extraction)
import requests  # For making HTTP requests to fetch web pages
from urllib.parse import urljoin # For joining relative and absolute URLs

def get_html_of(url):
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The decoded HTML content of the page.
             Exits the program if an HTTP error (non-200 status code) occurs.
    """
    resp = requests.get(url)  # Make the HTTP request to the specified URL

    if resp.status_code != 200:  # Check if the HTTP request was successful (status code 200 OK)
        print(f'\nHTTP status code {resp.status_code} returned, but 200 was expected. Exiting...\n')
        exit(1)  # Exit the program with an error code 

    return resp.content.decode()  # Decode the response content (usually from bytes to a string, typically UTF-8 encoding)

def get_all_words_from(url):
    """
    Extracts all words from the HTML content of a given URL.

    Args:
        url (str): The URL to fetch and extract words from.

    Returns:
        list: A list of words extracted from the webpage.
    """
    html = get_html_of(url)  # Fetch the HTML content of the URL
    soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content using BeautifulSoup's HTML parser
    raw_text = soup.get_text()  # Extract all text content from the HTML, discarding HTML tags
    
    return re.findall(r'\w+', raw_text)  # Find all 'words' (sequences of alphanumeric characters and underscores) using a regular expression

def count_occurrences_in(word_list, min_length):
    """
    Counts the occurrences of words in a list, considering only words of a minimum length.

    Args:
        word_list (list): A list of words (strings).
        min_length (int): The minimum length a word to be counted.

    Returns:
        dict: A dictionary where keys are words (of at least min_length) and values are their counts.
    """
    word_count = {}  # Initialize an empty dictionary to store word counts

    for word in word_list:  # Iterate through each word in the input word list
        if len(word) >= min_length:  # Check if the current word meets the minimum length requirement
            word_count[word] = word_count.get(word, 0) + 1  # Increment the count for the word.
                                                               # .get(word, 0) safely retrieves the current count (or 0 if word not yet in dict)
    
    return word_count  # Return the dictionary containing word counts

def crawl_website(start_url, depth, current_depth=0, visited=None):
    """
    Crawls a website starting from a given URL to a specified depth, extracting words from each page.

    Args:
        start_url (str): The URL to start crawling from.
        depth (int): The maximum depth to crawl. 0 means only the start_url is fetched.
        current_depth (int, optional): The current depth of crawling (used for recursion tracking). Defaults to 0.
        visited (set, optional): A set to keep track of visited URLs to avoid cycles. Defaults to None (initialized internally).

    Returns:
        list: A list of all words extracted from all crawled pages.
    """
    if visited is None:
        visited = set() # Initialize a set to keep track of visited URLs (for the first call)

    if current_depth > depth or start_url in visited: # Base cases for recursion: depth limit reached or URL already visited
        return [] # Stop crawling down this path

    visited.add(start_url) # Mark the current URL as visited to prevent re-visiting
    all_words = [] # Initialize a list to accumulate words from this URL and any URLs crawled from it

    print(f'Crawling... {start_url} (Depth: {current_depth})') # Provide feedback to the user about the crawling progress

    try:
        html = get_html_of(start_url) # Fetch the HTML content of the current URL
        all_words.extend(get_all_words_from(start_url)) # Extract words from the current URL and add them to the list

        if current_depth < depth: # If we are still within the crawling depth limit
            soup = BeautifulSoup(html, 'html.parser') # Parse the HTML content to find links
            for link in soup.find_all('a'): # Find all 'a' (anchor) tags, which represent links
                href = link.get('href') # Get the 'href' attribute of the link, which contains the URL
                if href: # Check if an 'href' attribute exists (some 'a' tags might not have them or have empty ones)
                    absolute_url = urljoin(start_url, href) # Construct the absolute URL by joining the base URL and the relative URL (href)
                    all_words.extend(crawl_website(absolute_url, depth, current_depth + 1, visited)) # Recursively crawl the linked URL, increasing the depth

    except requests.exceptions.RequestException as e: # Catch exceptions related to HTTP requests (e.g., connection errors, timeouts)
        print(f'Error crawling {start_url}: {e}') # Print an error message if crawling fails for a URL
    except Exception as e: # Catch any other potential exceptions during processing (e.g., HTML parsing errors)
        print(f'Error processing {start_url}: {e}') # Print a general error message

    return all_words # Return all words collected from this URL and recursively crawled URLs

def get_top_words_from(all_words, min_length):
    """
    Gets the top words from a list of words, sorted by frequency in descending order, considering minimum word length.

    Args:
        all_words (list): A list of all extracted words.
        min_length (int): The minimum length a word must have to be considered.

    Returns:
        list: A sorted list of tuples, where each tuple is (word, count),
              sorted in descending order of count.
    """
    occurrences = count_occurrences_in(all_words, min_length)  # Count the occurrences of words (meeting min_length)
    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)  # Sort the word-count pairs by count (the second item in the tuple), in reverse (descending) order

def generate_password_mutations(word):
    """
    Generates a list of common password mutations for a given word.

    Args:
        word (str): The word to generate mutations from.

    Returns:
        list: A sorted list of password mutations based on the input word.
    """
    mutations = set() # Use a set to store mutations to avoid duplicates
    mutations.add(word.capitalize()) # Add capitalized version (e.g., "word" -> "Word")
    mutations.add(word.lower())      # Add lowercase version (e.g., "WORD" -> "word")
    mutations.add(word.upper())      # Add uppercase version (e.g., "word" -> "WORD")

    current_year = datetime.datetime.now().year # Get the current year
    years = [str(current_year), str(current_year - 1), str(current_year - 2), str(current_year - 3), str(current_year - 4)] # List of current and past 4 years
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*'] # Common symbols used in passwords
    numbers = ['01', '123', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # Common number sequences/digits
    seasonal_words = ['Summer', 'Winter', 'Spring', 'Autumn', 'Fall'] # Seasonal words

    # Mutations by appending years and symbols
    for year in years:
        mutations.add(word + year) # word + year (e.g., word2023)
        for symbol in symbols:
            mutations.add(word + year + symbol) # word + year + symbol (e.g., word2023!)
            mutations.add(word + symbol + year) # word + symbol + year (e.g., word!2023)

    # Mutations by appending symbols and numbers
    for symbol in symbols:
        mutations.add(word + symbol) # word + symbol (e.g., word!)
        for number in numbers:
            mutations.add(word + symbol + number) # word + symbol + number (e.g., word!1)
            mutations.add(word + number + symbol) # word + number + symbol (e.g., word1!)
            mutations.add(word + number)        # word + number (e.g., word1)

    # Mutations combining seasonal words, years and the base word
    for season in seasonal_words:
        for year in years:
            mutations.add(season + word + year) # season + word + year (e.g., Summerword2023)
            mutations.add(word + season + year) # word + season + year (e.g., wordSummer2023)
            mutations.add(season + year + word) # season + year + word (e.g., Summer2023word)
            mutations.add(year + season + word) # year + season + word (e.g., 2023Summerword)
            mutations.add(word + year + season) # word + year + season (e.g., word2023Summer)
            mutations.add(year + word + season) # year + word + season (e.g., 2023wordSummer)

    number_sequences = ['01', '123'] # Common number sequences
    for num_seq in number_sequences:
        mutations.add(word + num_seq) # word + number sequence (e.g., word01)

    symbol_number_suffixes = ['1!', '2!', '3!'] # Common symbol-number suffixes
    for suffix in symbol_number_suffixes:
        mutations.add(word + suffix) # word + symbol-number suffix (e.g., word1!)

    return sorted(list(mutations)) # Convert the set of mutations to a sorted list and return it

# --- Command Line Interface using Click ---

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.') # URL option, prompted if not provided
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit)') # Minimum word length option, default 0
@click.option('--output', '-o', help='Output file to save results') # Output file path option
@click.option('--depth', '-d', default=0, help='Crawling depth (default: 0, only searches given URL') # Crawling depth option, default 0
@click.option('--mutate', '-m', is_flag=True, help='Generate and output common password mutations. ') # Mutate flag, if set password mutations will be generated
@click.option('--mutation-output', '-mo', help='Output file to save password mutations') # Mutation output file path option

def main(url, length, output, depth, mutate, mutation_output):
    """
    Web Crawler and Password Mutator Script.

    Crawls a website, extracts top words, and optionally generates password mutations.
    """
    the_words = crawl_website(url, depth)  # Extract all words from the specified URL and crawled pages
    top_words = get_top_words_from(the_words, length)  # Get the top words based on frequency and minimum length

    num_words_to_print = min(10, len(top_words)) # Determine the number of top words to print (max 10, or fewer if less than 10 words found)
    if not top_words: # If no words were found that meet the criteria
        print('\nNo words found matching the minimum length criteria\n')
    else: # If top words were found
        print('\nTOP WORDS')
        for i in range(num_words_to_print):
            print(f'{top_words[i][0]}: {top_words[i][1]}') # Print the top words and their counts

    mutated_passwords = {} # Initialize an empty dictionary to store mutated passwords
    if mutate: # If the mutate flag is set
        mutated_passwords = {} # Re-initialize (though already empty) to ensure clean state.
        for i in range(num_words_to_print): # Iterate through the top words
            word = top_words[i][0] # Get the word itself (not the count)
            mutations = generate_password_mutations(word) # Generate password mutations for the current word
            mutated_passwords[word] = mutations # Store the mutations in the dictionary, keyed by the original word

    if output: # If an output file path is specified
        try:
            with open(output, 'w') as wr: # Open the output file in write mode ('w')
                wr.write('TOP WORDS\n') # Write a header to the output file
                for word, count in top_words: # Iterate through the top words and their counts
                    wr.write(f'{word}: {count}\n') # Write each word and its count to the file

        except Exception as e: # Catch any exceptions that might occur during file writing
            print(f'Error writing to file: {e}') # Print an error message if writing fails

    if mutation_output: # If a mutation output file path is specified
        if mutate: # Check if mutation generation was actually enabled
            try:
                with open(mutation_output, 'w') as wr_mut: # Open the mutation output file in write mode ('w')
                    wr_mut.write('PASSWORD MUTATIONS\n') # Write a header to the mutation output file
                    for word, mutations in mutated_passwords.items(): # Iterate through the mutated passwords dictionary
                        wr_mut.write(f'\nMutations for {word}:\n') # Write a sub-header for each word's mutations
                        for mutation in mutations: # Iterate through the list of mutations for the current word
                            wr_mut.write(f' {mutation}\n') # Write each mutation to the file, indented for readability

            except Exception as e: # Catch any exceptions during mutation output file writing
                print(f'Error writing to mutation output file: {e}') # Print an error message
        else: # If mutation output file is specified but mutation generation was not enabled
            print('\nWarning: Mutation output file specified (--mutation-output), but mutation generation (--mutate) was not enabled. No mutations will be saved.')

if __name__ == '__main__':
    main()  # Run the main function when the script is executed directly
