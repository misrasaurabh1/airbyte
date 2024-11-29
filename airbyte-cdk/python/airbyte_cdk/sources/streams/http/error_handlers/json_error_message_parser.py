#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from typing import Optional

import requests
from airbyte_cdk.sources.streams.http.error_handlers import ErrorMessageParser
from airbyte_cdk.sources.utils.types import JsonType


class JsonErrorMessageParser(ErrorMessageParser):
    def _try_get_error(self, value: Optional[JsonType]) -> Optional[str]:
        if isinstance(value, str):
            return value
        elif isinstance(value, list):
            errors_in_value = filter(None, map(self._try_get_error, value))
            return ", ".join(errors_in_value)
        elif isinstance(value, dict):
            for key in self.keys_to_check:
                if key in value:
                    result = self._try_get_error(value[key])
                    if result:
                        return result
        return None

    def parse_response_error_message(self, response: requests.Response) -> Optional[str]:
        """
        Parses the raw response object from a failed request into a user-friendly error message.

        :param response:
        :return: A user-friendly message that indicates the cause of the error
        """
        try:
            body = response.json()
            return self._try_get_error(body)
        except requests.exceptions.JSONDecodeError:
            return None

    def __init__(self):
        self.keys_to_check = [
            "message",
            "messages",
            "error",
            "errors",
            "failures",
            "failure",
            "detail",
            "err",
            "error_message",
            "msg",
            "reason",
            "status_message",
        ]
