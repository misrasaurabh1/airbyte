#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


import re


# https://stackoverflow.com/a/1176023
def camel_to_snake(s: str) -> str:
    result = []
    for i, char in enumerate(s):
        if char.isupper():
            if i != 0 and (s[i - 1].islower() or (i + 1 < len(s) and s[i + 1].islower())):
                result.append("_")
            result.append(char.lower())
        else:
            result.append(char)
    return "".join(result)
