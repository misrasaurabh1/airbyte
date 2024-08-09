# Copyright (c) 2024 Airbyte, Inc., all rights reserved.

from airbyte_protocol.models import AirbyteMessage, Type

from airbyte_cdk.sources.connector_state_manager import HashableStreamDescriptor


def get_stream_descriptor(message: AirbyteMessage) -> HashableStreamDescriptor:
    msg_type = message.type
    if msg_type == Type.RECORD:
        return HashableStreamDescriptor(name=message.record.stream, namespace=message.record.namespace)
    elif msg_type == Type.STATE:
        state_stream = message.state.stream
        if not state_stream or not state_stream.stream_descriptor:
            raise ValueError("State message was not in per-stream state format, which is required for record counts.")
        return HashableStreamDescriptor(
            name=state_stream.stream_descriptor.name, namespace=state_stream.stream_descriptor.namespace
        )
    else:
        raise NotImplementedError(f"get_stream_descriptor is not implemented for message type '{msg_type}'.")
