"""Unit tests for config."""

from pathlib import Path

import pytest

from confluenceexport.config import (
    Config,
    JsonConfig,
    YamlConfig,
    load_config,
)
from confluenceexport.errors import ConfluenceExportError

#: Directory containing the configuration examples.
EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


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


def test_yaml_basic_config() -> None:
    """YAML basic config must be loaded without errors."""
    load_config(str(EXAMPLES_DIR / "basic_config.yaml"))


def test_json_basic_config() -> None:
    """JSON basic config must be loaded without errors."""
    load_config(str(EXAMPLES_DIR / "basic_config.json"))


def test_config_with_empty_config() -> None:
    """An empty config must raise an exception."""
    with pytest.raises(ConfluenceExportError):
        Config({})


@pytest.fixture
def full_config() -> dict:
    """Return a complete and valid configuration."""
    return {
        "Server": {"Confluence": "My confluence url"},
        "Pages to export": {
            "Space 1": ["Page 1.1"],
            "Space 2": ["Page 2.1", "Page 2.2"],
        },
    }


def test_config_without_server_config(full_config: dict) -> None:
    """A config without Server node must raise an exception."""
    del full_config["Server"]
    with pytest.raises(ConfluenceExportError):
        Config(full_config)


def test_config_without_server_confluence_config(full_config: dict) -> None:
    """A config without Server/Confluence node must raise an exception."""
    del full_config["Server"]["Confluence"]
    with pytest.raises(ConfluenceExportError):
        Config(full_config)


def test_config_with_server_confluence_config(full_config: dict) -> None:
    """A config with Server/Confluence node must return the right value."""
    config = Config(full_config)
    assert config.confluence == "My confluence url"


def test_config_without_pages_export_config(full_config: dict) -> None:
    """A config without Pages export node must raise an exception."""
    del full_config["Pages to export"]
    with pytest.raises(ConfluenceExportError):
        Config(full_config)
