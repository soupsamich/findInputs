import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import time
import logging
import os
import signal
import json

# Initialize data structure to store results
data = {"endpoints": []}

# Function to gracefully handle interruptions (Ctrl+C)
def save_and_exit(signum, frame):
    with open(args.output, 'w') as f:
        json.dump(data, f, indent=4)
    print("\nScript interrupted. Data saved to output file.")
    exit(0)

# Attach the signal handler for interruptions
signal.signal(signal.SIGINT, save_and_exit)

# Create a log file in the user's home directory
logfile = "~/findInputsLog.log"
logging.basicConfig(filename=os.path.expanduser(logfile), level=logging.DEBUG)

# Set up argument parser with necessary options
parser = argparse.ArgumentParser(
    description='Web crawler to find input fields',
    epilog='Example: python3 findInputs.py -u "https://www.example.com" -d "example.com" -he -un -t 0.8 -O "output.json"'
)
parser.add_argument('-u', '--url', required=True, help='The starting URL of the website to crawl')
parser.add_argument('-d', '--domain', required=True, help='The domain to restrict the crawl to')
parser.add_argument('-o', '--output', required=True, help='The output JSON file to write data')
parser.add_argument('-he', '--hide-empty', action='store_true', help='Hide endpoints with 0 input fields')
parser.add_argument('-un', '--unique', action='store_true', help='Show only unique input fields not seen before')
parser.add_argument('-t', '--rate-limit', type=float, default=0, help='Number of seconds to wait between requests')
args = parser.parse_args()

# ANSI escape codes for terminal text colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Request headers to help prevent 403 responses
# In the future this can be a list to randomly pick from
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36'
}

# A set to track visited URLs and unique input fields
visited = set()
unique_inputs = set()

# A function to create a unique identifier for an input field
def create_unique_id(input_field):
    return f"{input_field.get('id', '')}-{input_field.get('name', '')}-{input_field.get('type', '')}"

# Function to find input fields on a given page
def find_input_fields(url):
    try:
        response = requests.get(url, headers=headers)
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

        # Handle empty inputs based on the --hide-empty flag
        if not args.hide_empty or new_inputs:
            # Prepare data for JSON output
            endpoint_data = {
                "url": url,
                "inputs": [
                    {"id": inp.get('id', ''),
                     "type": inp.get('type', ''),
                     "name": inp.get('name', '')}
                    for inp in new_inputs
                ]
            }
            data["endpoints"].append(endpoint_data)

            # Incrementally write to JSON file
            with open(args.output, 'w') as f:
                json.dump(data, f, indent=4)

            # Print results to the terminal
            print(f"{GREEN}Found {len(new_inputs)} input fields on: {url}{RESET}")
            for i, inp in enumerate(new_inputs, start=1):
                input_id = inp.get('id', 'not specified')
                input_type = inp.get('type', 'not specified')
                input_name = inp.get('name', 'not specified')
                print(f"Input {i} {BLUE}ID:{RESET} {input_id}, {RED}Type:{RESET} {input_type}, {YELLOW}Name:{RESET} {input_name}")
    except Exception as e:
        logging.info(f"Error processing {url}: {e}")

# Function to get all links from a webpage
def get_all_links(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Resolve relative links to absolute URLs
            if not href.startswith('http'):
                href = urljoin(url, href)
            if args.domain in href and href not in visited:
                visited.add(href)
                yield href
    except Exception as e:
        logging.info(f"Error fetching links from {url}: {e}")

# Recursive function to crawl the website
def crawl(url):
    for link in get_all_links(url):
        find_input_fields(link)
        time.sleep(args.rate_limit)  # Respect rate limit between requests
        crawl(link)

# Start crawling from the initial URL
try:
    crawl(args.url)
except Exception as e:
    logging.info(f"Script error: {e}")
