#! python3

"""
Main entry point to extract Confluence pages.
"""

import argparse
import logging
import os
import sys
from dotenv import load_dotenv
from .config import load_config
from .confluenceclient import ConfluenceClient
from .export import export_all_pages


def _create_argument_parser() -> argparse.ArgumentParser:
    """
    Create the list of arguments supported and return the parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose mode",
        dest="verbose",
    )
    parser.add_argument(
        "config",
        action="store",
        help="Configuration file",
        nargs="?",
        metavar="config.yaml",
    )
    return parser


def main() -> None:
    """
    Entry point of Confluence extractor script.
    """
    # Parse command line
    parser = _create_argument_parser()
    args = parser.parse_args()

    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Create logger
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=log_level,
    )

    if not args.config:
        parser.print_usage()
        return

    # Get configuration from JSON/YAML file
    config = load_config(args.config)
    if args.verbose:
        config.dump()

    # Retrieve Atlassian secrets from .env or environment variables
    load_dotenv()

    confluence_client = ConfluenceClient(
        config.confluence,
        os.environ["ATLASSIAN_USER"],
        os.environ["ATLASSIAN_TOKEN"],
    )

    export_all_pages(confluence_client, config)
