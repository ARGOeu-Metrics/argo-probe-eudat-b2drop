# argo-probe-eudat-b2drop
A script to monitor status of B2DROP.B2DROP B2DROP is a low-barrier, user-friendly and trustworthy storage environment which allows users to synchronise their active data across different desktops and to easily share this data with peers.

## Usage
``b2drop.py [-h] --probe PROBE [--url URL] [--username USERNAME] [--password PASSWORD] [--config CONFIG]``


b2drop probe for different checks over webdav

 ### Required options:


 `--probe PROBE`        Type of test-probe, e.g. 'upload', 'download', 'checksum'
 
 `--url URL`            The URL to connect to.
 
 `--username USERNAME`  The username for authentication.
 
 `--password PASSWORD`  The password for authentication.

You can have multiple probing options:

- upload: Test if uploading is working
- download: Test that downloading is working, implies uploading is working
- checksum: Download and Upload a file and checks if their checksums match
- delete: Tests if deleting an uploaded file works


 ### Optional options:
 
 `--config CONFIG`      Optional config file to load parameters from.
 
 ` -h, --help`           show this help message and exit


#### Config file

Alternatively you can use a config file with the name `config.json` with the following format
```
{
    "url": "https://b2drop.eudat.eu",
    "username": "your_b2drop_app_token_name",
    "password": "your_b2drop_app_token_credentials"
}
```
