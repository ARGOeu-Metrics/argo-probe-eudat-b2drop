#! /usr/bin/env python3

import argparse
import json
import os
import sys
from b2drop_api import B2dropClient
from probes import probe_upload, probe_up_and_download, probe_checksum, probe_delete, probe_all_actions
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/var/spool/argo/probes/eudat-b2drop/debug.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def load_config(config_file='config.json'):
    """Loads configuration from a JSON file."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError as e:
                logger.error("Invalid Json file")
                logger.error(str(e))
                print ("CRITICAL: Invalid Json file")
                sys.exit(2)
    return None


def main(args):
    # Load from config file if arguments are not provided
    if not args.url or not args.username or not args.password:
        if not args.config:
            logger.error("You either need to set 'url', 'username' and 'password' or set up a config and use 'config'!")
            print ("You either need to set 'url', 'username' and 'password' or set up a config and use 'config'!")
            sys.exit(2)
        config = load_config(args.config)
        if config:
            url = config.get('url', args.url)
            username = config.get('username', args.username)
            password = config.get('password', args.password)
        else:
            logger.error(f"Config file {args.config} not found or incomplete.")
            print ("CRITICAL: Config file not found or incomplete or username or password is missing.")
            sys.exit(2)
    else:
        url, username, password = args.url, args.username, args.password

    # set up b2dropclient
    client = B2dropClient(url, username, password)

    # start probe
    success: bool = False
    if args.probe == "download":
        success = probe_up_and_download(client)
    elif args.probe == "upload":
        success = probe_upload(client)
    elif args.probe == "checksum":
        success = probe_checksum(client)
    elif args.probe == "all":
        success = probe_all_actions(client)
    elif args.probe == "delete":
        success = probe_delete(client)
    else:
        logger.error(f"Unknown probe type '{args.probe}'!")
        print ("CRITICAL: Unknown probe type.")
        sys.exit(2)

    client.cleanup()

    if not success:
        logger.error(f"Test was not successful!")
        print ("CRITICAL: Test was not successful.")
        sys.exit(2)
    else:
        logger.info(f"Test was successful!")
        print ("OK: Test was successful!")
        sys.exit(0)
    return success


if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="b2drop probe for different checks over webdav")
    parser.add_argument('--probe', required=True, type=str,
                        help="Type of test-probe, e.g. 'upload', 'download', 'checksum','all'")
    parser.add_argument('--url', required=False, type=str, help="The URL to connect to.")
    parser.add_argument('--username', required=False, type=str, help="The username for authentication.")
    parser.add_argument('--password', required=False, type=str, help="The password for authentication.")
    parser.add_argument('--config', required=False, type=str, default='config.json',
                        help="Optional config file to load parameters from.")

    args = parser.parse_args()
    ret = main(args)
    exit(ret)
