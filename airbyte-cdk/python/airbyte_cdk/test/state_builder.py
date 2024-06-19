# Copyright (c) 2023 Airbyte, Inc., all rights reserved.

from typing import Any, List

from airbyte_protocol.models import AirbyteStateMessage


class StateBuilder:
    def __init__(self) -> None:
        self._state: List[AirbyteStateMessage] = []

    def with_stream_state(self, stream_name: str, state: Any) -> "StateBuilder":
        stream_state = {"type": "STREAM", "stream": {"stream_state": state, "stream_descriptor": {"name": stream_name}}}
        self._state.append(AirbyteStateMessage(**stream_state))
        return self

    def build(self) -> List[AirbyteStateMessage]:
        return self._state
