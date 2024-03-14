# Find Inputs

Use findInputs.py to crawl a website's endpoints and return any input fields


## Recommended Python Version:

findInputs currently supports **Python 2** and **Python 3**.

* The recommended version for Python 2 is **2.7.x**
* The recommended version for Python 3 is **3.4.x**

## Dependencies:

findInputs depends on the `requests`, `BeautifulSoup`, `argparse` and `time` python modules.

Each module can be installed independently as shown below.

#### Requests, BeautifulSoup, and ArgParse Modules (http://docs.python-requests.org/en/latest/)

- Install for Windows:
```
c:\python38\python3.exe -m pip3 install requests beautifulsoup4
```

- Install using pip on Linux:
```
sudo pip3 install requests beautifulsoup4 argparse
```

## Usage

Short Form    | Long Form     | Description
------------- | ------------- |-------------
-h            | --help        | Show the help message and exit
-u            | --url         | Starting URL to crawl from
-d            | --domain      | Stay within this domain when following links
-he           | --hide-empty  | Hide endpoints with 0 input fields
-un           | --unique      | Only show inputs that haven't been seen before
-t            | --rate-limit  | Number of seconds to wait between requests

### Examples

* To return any input fields found within the specified domain:

```python3 findInputs.py -u "https://www.example.com" -d "example.com"```

* Return input fields, but exclude endpoints that return 0, and only show unique inputs:

``python3 findInputs.py -u "https://www.example.com" -d "example.com" -he -un``


## License

This project is licensed under the GPL-3.0 License - see the LICENSE.md file for details

## Version
**Current version is 1.0**
