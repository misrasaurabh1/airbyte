# Copyright (c) 2024 Airbyte, Inc., all rights reserved.

from airbyte_cdk.models import AirbyteMessage, Type


def get_stream_descriptor(message: AirbyteMessage) -> tuple[str, str | None]:
    match message.type:
        case Type.RECORD:
            return (message.record.stream, message.record.namespace)  # type: ignore[union-attr] # record has `stream` and `namespace`
        case Type.STATE:
            if not message.state.stream or not message.state.stream.stream_descriptor:  # type: ignore[union-attr] # state has `stream`
                raise ValueError("State message was not in per-stream state format, which is required for record counts.")
            return (message.state.stream.stream_descriptor.name, message.state.stream.stream_descriptor.namespace)  # type: ignore[union-attr] # state has `stream`
        case _:
            raise NotImplementedError(f"get_stream_descriptor is not implemented for message type '{message.type}'.")
