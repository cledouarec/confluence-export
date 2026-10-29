#! python3

"""Unit tests for confluenceclient."""

import pytest
from confluenceexport.confluenceclient import ConfluenceClient
from confluenceexport.errors import ConfluenceExportError


def test_create_confluence_client_with_empty_url() -> None:
    """Confluence client creation with invalid url must raise an error."""
    with pytest.raises(ConfluenceExportError):
        ConfluenceClient("", "user", "pass")


def test_create_confluence_client_with_empty_username() -> None:
    """Confluence client creation with invalid username must raise an error."""
    with pytest.raises(ConfluenceExportError):
        ConfluenceClient("http://test", "", "pass")


def test_create_confluence_client_with_empty_password() -> None:
    """Confluence client creation with invalid password must raise an error."""
    with pytest.raises(ConfluenceExportError):
        ConfluenceClient("http://test", "user", "")
