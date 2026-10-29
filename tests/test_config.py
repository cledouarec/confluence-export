#! python3

"""Unit tests for config."""

import pytest
from confluenceexport.config import (
    Config,
    JsonConfig,
    YamlConfig,
    load_config,
)
from confluenceexport.errors import ConfluenceExportError


@pytest.fixture(scope="module")
def script_loc(request):
    """
    Return the directory of the currently running test script.
    """

    # uses .join instead of .dirname so we get a LocalPath object instead of
    # a string. LocalPath.join calls normpath for us when joining the path
    return request.fspath.join("..")


def test_load_config_with_invalid_file_extension() -> None:
    """Loads config with unsupported file extension must raise an exception."""
    with pytest.raises(ConfluenceExportError):
        load_config("config.test")


def test_yaml_config_with_invalid_file() -> None:
    """Read YAML config without file name must raise an exception."""
    with pytest.raises(ConfluenceExportError):
        YamlConfig("")


def test_json_config_with_invalid_file() -> None:
    """Read JSON config without file name must raise an exception."""
    with pytest.raises(ConfluenceExportError):
        JsonConfig("")


def test_yaml_basic_config(script_loc) -> None:
    """YAML basic config must be loaded without errors."""
    config = script_loc.join("../examples/basic_config.yaml")
    load_config(config)


def test_json_basic_config(script_loc) -> None:
    """JSON basic config must be loaded without errors."""
    config = script_loc.join("../examples/basic_config.json")
    load_config(config)


def test_config_with_empty_config() -> None:
    """An empty config must raise an exception."""
    with pytest.raises(ConfluenceExportError):
        Config({})


@pytest.fixture
def full_config():
    """Return a complete and valid configuration."""
    return {
        "Server": {"Confluence": "My confluence url"},
        "Pages to export": {
            "Space 1": ["Page 1.1"],
            "Space 2": ["Page 2.1", "Page 2.2"],
        },
    }


def test_config_without_server_config(full_config) -> None:
    """A config without Server node must raise an exception."""
    del full_config["Server"]
    with pytest.raises(ConfluenceExportError):
        Config(full_config)


def test_config_without_server_confluence_config(full_config) -> None:
    """A config without Server/Confluence node must raise an exception."""
    del full_config["Server"]["Confluence"]
    with pytest.raises(ConfluenceExportError):
        Config(full_config)


def test_config_with_server_confluence_config(full_config) -> None:
    """A config with Server/Confluence node must return the right value."""
    config = Config(full_config)
    assert config.confluence == "My confluence url"


def test_config_without_pages_export_config(full_config) -> None:
    """A config without Pages export node must raise an exception."""
    del full_config["Pages to export"]
    with pytest.raises(ConfluenceExportError):
        Config(full_config)
