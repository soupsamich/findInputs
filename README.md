# Find Inputs

Use findInputs.py to crawl a website's endpoints and return any input fields


## Recommended Python Version:

findInputs currently supports **Python 2** and **Python 3**.

* The recommended version for Python 2 is **2.7.x**
* The recommended version for Python 3 is **3.4.x**

## Dependencies:

findInputs depends on the `requests`, `BeautifulSoup`, `argparse`, `time`, `logging`, and `os` python modules.

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

## Usage:

Short Form    | Long Form     | Description
------------- | ------------- |-------------
-h            | --help        | Show the help message and exit
-t            | --target      | Starting URL to crawl from
-s            | --scope       | Stay within this domain when following links
-o            | --output      | The output JSON file to write data
-he           | --hide-empty  | Hide endpoints with 0 input fields
-un           | --unique      | Only show inputs that haven't been seen before
-r            | --rate-limit  | Number of seconds to wait between requests

### Examples

* To return any input fields found on the target website within scope:

```python3 findInputs.py -t "https://www.example.com" -s "example.com"```

* Return input fields on the target website within scope, but exclude endpoints that return 0 inputs, only show inputs that we haven't seen on other endpoints already, rate limit requests to 0.8 seconds, and output the data to output.json file:

```python3 findInputs.py -t "https://www.example.com" -s "example.com" -he -un -r 0.8 -o "output.json"```


## Logging:
A log file will be created in the current user's home directory with the name `findInputsLog.log`

## License:

This project is licensed under the GPL-3.0 License - see the LICENSE.md file for details

## Version:
**Current version is 1.0**
