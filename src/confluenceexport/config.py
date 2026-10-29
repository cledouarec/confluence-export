#! python3

"""Manage configuration file."""

import json
import logging
import pathlib
import yaml
from .errors import ConfluenceExportError
from .utils import force_list, keys_exists

#: Create logger for this file.
logger = logging.getLogger()


class Config:
    """This class is used to manage configuration."""

    def __init__(self, config: dict):
        """Constructs the configuration from dictionary.

        Args:
            config: Configuration dictionary.
        """
        logger.debug("Create configuration")

        Config._check_config(config)

        #: Configuration dictionary already parsed
        self._config: dict = config

        # Convert all pages to list
        for space, titles in self._config["Pages to export"].items():
            self._config["Pages to export"][space] = force_list(titles)

        logger.debug("Configuration created")

    @staticmethod
    def _check_config(config: dict) -> None:
        """Check that the configuration contains all mandatory fields.

        Args:
            config: Configuration dictionary.

        Raises:
            ConfluenceExportError: If configuration is invalid.
        """
        if not keys_exists(config, "Server"):
            msg = "Missing Server node in configuration"
            raise ConfluenceExportError(msg)
        if not keys_exists(config, "Server", "Confluence"):
            msg = "Missing Confluence server configuration"
            raise ConfluenceExportError(msg)
        if not keys_exists(config, "Pages to export"):
            msg = "Missing Projects node configuration"
            raise ConfluenceExportError(msg)

    def dump(self) -> None:
        """Dump the configuration."""
        print(self._config)

    @property
    def confluence(self) -> str:
        """Confluence server URL."""
        return self._config["Server"]["Confluence"]

    @property
    def pages_to_export(self) -> dict:
        """Pages to export, grouped by Confluence space."""
        return self._config["Pages to export"]


class YamlConfig(Config):
    """This class is used to manage YAML configuration."""

    def __init__(self, yaml_config_file: str):
        """Constructs the configuration from YAML file.

        Args:
            yaml_config_file: YAML configuration file to parse.

        Raises:
            ConfluenceExportError: If configuration file is invalid.
        """
        logger.info("Parse YAML configuration from %s", yaml_config_file)

        try:
            with open(yaml_config_file, encoding="utf-8") as yaml_config:
                super().__init__(yaml.safe_load(yaml_config))
        except Exception as error:
            msg = "Failed to parse YAML configuration"
            raise ConfluenceExportError(msg) from error

        logger.info("Configuration YAML parsed")


class JsonConfig(Config):
    """This class is used to manage JSON configuration."""

    def __init__(self, json_config_file: str):
        """Constructs the configuration from JSON file.

        Args:
            json_config_file: JSON configuration file to parse.

        Raises:
            ConfluenceExportError: If configuration file is invalid.
        """
        logger.info("Parse JSON configuration from %s", json_config_file)

        try:
            with open(json_config_file, encoding="utf-8") as json_config:
                super().__init__(json.load(json_config))
        except Exception as error:
            msg = "Failed to parse JSON configuration"
            raise ConfluenceExportError(msg) from error

        logger.info("Configuration JSON parsed")


def load_config(config_file: str) -> Config:
    """Loads the configuration file (JSON or YAML).

    Args:
        config_file: Configuration file to parse.

    Returns:
        Configuration parsed.

    Raises:
        ConfluenceExportError: If configuration extension file is unknown
            (.json, .yaml, .yml).
    """
    config_type = pathlib.Path(config_file).suffix
    if config_type in [".yaml", ".yml"]:
        return YamlConfig(config_file)
    if config_type == ".json":
        return JsonConfig(config_file)
    msg = "Unknown file extension for configuration"
    raise ConfluenceExportError(msg)
