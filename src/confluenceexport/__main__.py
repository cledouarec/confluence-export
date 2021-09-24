#! python3

"""
Main script entry point to extract Confluence pages.
"""

from confluenceexport.cli import main


if __name__ == "__main__":
    # Entry point of Confluence extractor script.
    # Execute only if run as a script.
    main()
