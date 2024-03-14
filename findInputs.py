import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import time

# Set up the argument parser
parser = argparse.ArgumentParser(
    description='Web crawler to find input fields',
    epilog='Example: python3 findInputs.py -u "https://www.example.com" -d "example.com" -he -un -t 0.8')
parser.add_argument('-u', '--url', required=True, help='The starting URL of the website to crawl')
parser.add_argument('-d', '--domain', required=True, help='The domain to restrict the crawl to')
parser.add_argument('-he', '--hide-empty', action='store_true', help='Hide endpoints with 0 input fields')
parser.add_argument('-un', '--unique', action='store_true', help='Show only unique input fields not seen before')
parser.add_argument('-t', '--rate-limit', type=float, default=0, help='Number of seconds to wait between requests')
args = parser.parse_args()

# A set to keep track of visited URLs and unique input fields
visited = set()
unique_inputs = set()

# A function to create a unique identifier for an input field
def create_unique_id(input_field):
    return f"{input_field.get('id', '')}-{input_field.get('name', '')}-{input_field.get('type', '')}"

# ANSI escape codes for colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# A function to find all the input fields in a given page
def find_input_fields(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    inputs = soup.find_all('input')
    new_inputs = []
    
    # Filter for unique inputs if the --unique flag is set
    if args.unique:
        for inp in inputs:
            unique_id = create_unique_id(inp)
            if unique_id not in unique_inputs:
                unique_inputs.add(unique_id)
                new_inputs.append(inp)
    else:
        new_inputs = inputs
    
    # Print the inputs if not hiding empty, or if they are new inputs to show
    if not args.hide_empty or new_inputs:
        print(f"{GREEN}Found {len(new_inputs)} input fields on: {url}{RESET}")
        for i, inp in enumerate(new_inputs, start=1):
        # Print with colors
            input_id = inp.get('id', 'not specified')
            input_type = inp.get('type', 'not specified')
            input_name = inp.get('name', 'not specified')
            print(f"Input {i} {BLUE}ID:{RESET} {input_id}, {RED}Type:{RESET} {input_type}, {YELLOW}Name:{RESET} {input_name}")

# A function to get all the links from a webpage
def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        if not href.startswith('http'):
            href = urljoin(url, href)
        if args.domain in href and href not in visited:
            visited.add(href)
            yield href

# A function to crawl the website
def crawl(url):
    for link in get_all_links(url):
        find_input_fields(link)
        time.sleep(args.rate_limit) # wait specified number of seconds
        crawl(link)

# Start crawling from the initial URL
crawl(args.url)
