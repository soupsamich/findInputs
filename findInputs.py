import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse

# Set up the argument parser
parser = argparse.ArgumentParser(
    description='Web crawler to find input fields',
    epilog='Example: python3 findInputs.py -u "https://www.example.com" -d "example.com" -he')
parser.add_argument('-u', '--url', required=True, help='The starting URL of the website to crawl')
parser.add_argument('-d', '--domain', required=True, help='The domain to restrict the crawl to')
parser.add_argument('-he', '--hide-empty', action='store_true', help='Hide endpoints with 0 input fields')
args = parser.parse_args()

# A set to keep track of visited URLs
visited = set()

# ANSI escape codes for colors
RED = '\033[91M'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# A function to find all the input fields in a given page
def find_input_fields(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    inputs = soup.find_all('input')
    if not args.hide_empty or (args.hide_empty and inputs):
        print(f"{GREEN}Found {len(inputs)} input fields on: {url}{RESET}")
        for i, inp in enumerate(inputs, start=1):
        # Print input type in red and input name in yellow
            input_type = inp.get('type', 'not specified')
            input_name = inp.get('name', 'not specified')
            print(f"{RED}Input {i} Type: {input_type}{RESET}, {YELLOW}Name: {input_name}{RESET}")

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
        crawl(link)

# Start crawling from the initial URL
crawl(args.url)
