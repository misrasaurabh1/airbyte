#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


from typing import Any, List, Mapping, Optional, Set, Union


def combine_mappings(mappings: List[Optional[Union[Mapping[str, Any], str]]]) -> Union[Mapping[str, Any], str]:
    """
    Combine multiple mappings into a single mapping. If any of the mappings are a string, return
    that string. Raise errors in the following cases:
    * If there are duplicate keys across mappings
    * If there are multiple string mappings
    * If there are multiple mappings containing keys and one of them is a string
    """
    combined_mapping = {}
    keys_seen = set()
    string_mapping = None
    string_count = 0

    for part in mappings:
        if part is None:
            continue

        if isinstance(part, str):
            string_count += 1
            if string_count > 1:
                raise ValueError("Cannot combine multiple string options")
            string_mapping = part
        else:
            for key in part:
                if key in keys_seen:
                    raise ValueError(f"Duplicate key found: {key}")
                keys_seen.add(key)
            combined_mapping.update(part)

    if string_mapping is not None:
        if combined_mapping:
            raise ValueError("Cannot combine multiple options if one is a string")
        return string_mapping

    return combined_mapping
