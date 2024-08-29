#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Union

from airbyte_cdk.sources.types import StreamSlice, StreamState


@dataclass
class RequestOptionsProvider:
    """
    Defines the request options to set on an outgoing HTTP request

    Options can be passed by
    - request parameter
    - request headers
    - body data
    - json content
    """

    @abstractmethod
    def get_request_params(
        self,
        *,
        stream_state: Optional[StreamState] = None,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Mapping[str, Any]:
        """
        Specifies the query parameters that should be set on an outgoing HTTP request given the inputs.

        E.g: you might want to define query parameters for paging if next_page_token is not None.
        """
        pass

    @abstractmethod
    def get_request_headers(
        self,
        *,
        stream_state: Optional[StreamState] = None,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Mapping[str, Any]:
        """Return any non-auth headers. Authentication headers will overwrite any overlapping headers returned from this method."""

    @abstractmethod
    def get_request_body_data(
        self,
        *,
        stream_state: Optional[StreamState] = None,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Union[Mapping[str, Any], str]:
        """
        Specifies how to populate the body of the request with a non-JSON payload.

        If returns a ready text that it will be sent as is.
        If returns a dict that it will be converted to a urlencoded form.
        E.g. {"key1": "value1", "key2": "value2"} => "key1=value1&key2=value2"

        At the same time only one of the 'request_body_data' and 'request_body_json' functions can be overridden.
        """

    def get_request_body_json(
        self,
        *,
        stream_state: Optional[StreamState] = None,
        stream_slice: Optional[StreamSlice] = None,
        next_page_token: Optional[Mapping[str, Any]] = None,
    ) -> Mapping[str, Any]:
        if stream_slice is None:
            raise ValueError("A partition needs to be provided in order to get request body json")

        partition_key = self._to_partition_key(stream_slice.partition)
        partition_cursor = self._cursor_per_partition.get(partition_key)
        if partition_cursor is None:
            partition_cursor = self._cursor_factory.create_cursor()
            self._cursor_per_partition[partition_key] = partition_cursor

        partition_request_body = self._partition_router.get_request_body_json(
            stream_state=stream_state,
            stream_slice=StreamSlice(partition=stream_slice.partition, cursor_slice={}),
            next_page_token=next_page_token,
        )
        cursor_request_body = partition_cursor.get_request_body_json(
            stream_state=stream_state,
            stream_slice=StreamSlice(partition={}, cursor_slice=stream_slice.cursor_slice),
            next_page_token=next_page_token,
        )

        return {**partition_request_body, **cursor_request_body}
