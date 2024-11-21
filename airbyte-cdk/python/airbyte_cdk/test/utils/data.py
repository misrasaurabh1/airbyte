# Copyright (c) 2024 Airbyte, Inc., all rights reserved.

import os

from pydantic import FilePath


def get_unit_test_folder(execution_folder: str) -> FilePath:
    path = os.path.abspath(execution_folder)
    while True:
        if os.path.basename(path) == "unit_tests":
            return FilePath(path)
        new_path = os.path.dirname(path)
        if new_path == path:
            raise ValueError(f"Could not find `unit_tests` folder as a parent of {execution_folder}")
        path = new_path


def read_resource_file_contents(resource: str, test_location: str) -> str:
    """Read the contents of a test data file from the test resource folder."""
    file_path = str(get_unit_test_folder(test_location) / "resource" / "http" / "response" / f"{resource}")
    with open(file_path) as f:
        response = f.read()
    return response
