#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations
import pkgutil
from typing import Any

import yaml
from airbyte_cdk.sources.declarative.manifest_declarative_source import ManifestDeclarativeSource
from airbyte_cdk.sources.types import ConnectionDefinition


class YamlDeclarativeSource(ManifestDeclarativeSource):
    """Declarative source defined by a yaml file"""

    def __init__(self, path_to_yaml: str, debug: bool = False) -> None:
        """
        :param path_to_yaml: Path to the yaml file describing the source
        """
        self._path_to_yaml = path_to_yaml
        source_config = self._read_and_parse_yaml_file(path_to_yaml)
        super().__init__(source_config, debug)

    def _read_and_parse_yaml_file(self, path_to_yaml_file: str) -> ConnectionDefinition:
        package = self.__class__.__module__.split(".")[0]

        yaml_config = pkgutil.get_data(package, path_to_yaml_file)
        if yaml_config:
            decoded_yaml = yaml_config.decode()
            return self._parse(decoded_yaml)
        else:
            return {}

    def _emit_manifest_debug_message(self, extra_args: dict[str, Any]) -> None:
        extra_args["path_to_yaml"] = self._path_to_yaml
        self.logger.debug("declarative source created from parsed YAML manifest", extra=extra_args)

    @staticmethod
    def _parse(connection_definition_str: str) -> ConnectionDefinition:
        """
        Parses a yaml file into a manifest. Component references still exist in the manifest which will be
        resolved during the creating of the DeclarativeSource.
        :param connection_definition_str: yaml string to parse
        :return: The ConnectionDefinition parsed from connection_definition_str
        """
        return yaml.load(connection_definition_str, Loader=yaml.CSafeLoader)  # use CSafeLoader if available

    def _read_and_parse_yaml_file(self, path_to_yaml: str) -> ConnectionDefinition:
        """
        Reads and parses a yaml file
        :param path_to_yaml: Path to the yaml file to read and parse
        :return: The parsed yaml as a ConnectionDefinition
        """
        with open(path_to_yaml, "rb") as file:  # open file in binary mode
            connection_definition_str = file.read()
        return self._parse(connection_definition_str)
