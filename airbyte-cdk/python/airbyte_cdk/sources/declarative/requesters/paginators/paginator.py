#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping, Optional

import requests
from airbyte_cdk.sources.declarative.requesters.request_options.request_options_provider import RequestOptionsProvider
from airbyte_cdk.sources.types import Record


@dataclass
class Paginator(ABC, RequestOptionsProvider):
    """
    Defines the token to use to fetch the next page of records from the API.

    If needed, the Paginator will set request options to be set on the HTTP request to fetch the next page of records.
    If the next_page_token is the path to the next page of records, then it should be accessed through the `path` method
    """

    @abstractmethod
    def reset(self, reset_value: Optional[Any] = None) -> None:
        """
        Reset the pagination's inner state
        """

    def next_page_token(
        self, response: requests.Response, last_page_size: int, last_record: Optional[Record]
    ) -> Optional[Mapping[str, Any]]:
        if self._page_count >= self._maximum_number_of_pages:
            return None

        self._page_count += 1
        return self._decorated.next_page_token(response, last_page_size, last_record)

    @abstractmethod
    def path(self) -> Optional[str]:
        """
        Returns the URL path to hit to fetch the next page of records

        e.g: if you wanted to hit https://myapi.com/v1/some_entity then this will return "some_entity"

        :return: path to hit to fetch the next request. Returning None means the path is not defined by the next_page_token
        """
        pass
