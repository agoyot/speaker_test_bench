""" Script containing utilitary function/class
"""
import json
import math
import sys
from math import isnan, isinf
from collections.abc import Iterable
from datetime import datetime
from enum import Enum
from typing import Any, Union

import arrow
import numpy as np
import pandas as pd


def copy_key_content(
    src_dict: dict, target_dict: dict, key: str, inplace: bool
):
    """Copy the content of a dictionary into another one.

    Args:
        src_dict (dict): dictionary in which to get data from
        target_dict (dict): dictionary to be updated with data from source
        key (str): key to fetch in the source to copy in the target
        inplace (bool): flag to indicate to if the dictionary target_dict must
         be modified or a new dictionary must be returned (dictionaries are
         passed by reference in Python). This behavior mimics the one of the
         Pandas API.

    Returns:
        Copy of the dictionary when specified

    Raises:
        KeyError: raised when the 'key' is not found in source
    """
    # Check if key is present in the source dictionary
    if src_dict.get(key, None) is not None:
        # Check if key already exist in the target dictionary
        if target_dict.get(key, None) is not None:
            # If already exist, simply update the dictionary
            target_dict[key].update(src_dict[key])
        else:
            target_dict[key] = src_dict[key]
    else:
        raise KeyError(f"{key} key not found in input dictionary")

    if not inplace:
        return target_dict.copy()


class ExtendedEnum(Enum):
    """Mother enumeration class developed to provide special methods to
    enumeration types inheriting from it."""

    @classmethod
    def list(cls) -> list:
        """Produce a list with all the attributes from an enum class.

        Returns:
             List of attributes of the enum class
        """
        return list(map(lambda x: x.value, cls))

    @classmethod
    def tuple(cls) -> tuple:
        """Produce a tuple with all the attributes from an enum class.

        Returns:
             Tuple of attributes of the enum class
        """
        return tuple(map(lambda x: x.value, cls))

    @classmethod
    def print(cls) -> str:
        """Produce a string with all the attributes from an enum class.

        Returns:
             String of attributes of the enum class
        """
        return str(tuple(map(lambda x: x.value, cls)))


class CustomEncoder(json.JSONEncoder):
    """Extend the behavior the JSONEncoder class.

    The formatted JSON must comply with several guidelines in order to prevent
    problems later in the processing pipeline. This class adds user defined
    functionalities to the JSONEncoder usual behavior.

    Notes:
        It is preferable to modify each problem with compatibility type from
        Python to JSON in this class rather than adding conversions inside the
        Python main code.

    Example:
        Line of code to use to export a Python dictionary to JSON string.
        json.dumps(python_dict, separators=(',', ':'), cls=CustomEncoder)
    """

    def __init__(self, *args, **kwargs):
        """Principle class constructor."""
        super().__init__(*args, **kwargs)
        self.naninf_replacement = None

    def encode(self, obj):
        """Overrides the encode() method.

        Notes::
            Recursive method is called for every object that is usually
            serializable by the class JSONEncoder
        """

        def naninf_to_none(o):
            """Implement every specific processing to do for every serializable
            object."""
            if isinstance(o, float) and math.isnan(o):
                return self.naninf_replacement
            elif isinstance(o, float) and math.isinf(o):
                # Replace inf and -inf floats
                return self.naninf_replacement
            # Recursive replace in dict, list, tuple, np.ndarray
            elif isinstance(o, dict):
                return {k: naninf_to_none(v) for k, v in o.items()}
            elif isinstance(o, (list, tuple, np.ndarray)):
                return [naninf_to_none(e) for e in o]
            elif isinstance(o, bytes):
                # Prevent circular reference when converting byte objects
                return o.decode()
            else:
                return o

        return super().encode(naninf_to_none(obj))

    def default(self, obj):
        """Overloading the default behavior of the JSONEncoder default method.

        Args:
            obj: Object tested in the conversion process.

        Notes:
            This function is called for every object that is not serializable.
            For example, it is impossible to change the encoding behavior of
            strings or dictionaries in the current JSON implementation.
        """
        if isinstance(obj, arrow.Arrow):
            return obj.for_json()
        elif isinstance(obj, (datetime, np.datetime64)):
            # Convert first to pandas Timestamp for compatibility
            return arrow.get(pd.Timestamp(obj)).for_json()
        elif isinstance(obj, np.generic):
            return obj.item()
        elif isinstance(obj, pd.Series):
            # Convert series object to list
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict()
        else:
            # Default behavior when non-serializable objects type was not taken
            # into account previously. Supposed to supersede the option
            # 'default=str' in the native json.dump() function.
            return str(obj)


def flatten(in_list: Union[list, Iterable]) -> list:
    """Flat a list composed of unknown number of nested objects.

    Args:
        in_list (list): list to be flattened, it can be composed of
         dictionaries, lists, strings or other types

    Returns:
        out_list: a list without nested elements

    Notes:
        dictionaries, strings and bytes are replicated as is inside the
        resulting list output.
    """
    out_list = []
    for obj in in_list:
        # Check object type and prevent looping through string characters
        if isinstance(obj, Iterable) and not isinstance(
            obj, (str, bytes, dict)
        ):
            out_list.extend(flatten(obj))
        else:
            out_list.append(obj)
    return out_list


def check_timestamp_iso(date: str) -> bool:
    """Test if the value is transformable into ISO 8601 date format i.e. YYYY-
    MM-DDTHH:mm:SS.SSS+XX:00 or YYYY-MM-DDTHH:mm:SS.SSSSSS+XX:00 or YYYY-MM-DD
    HH:mm:SS+XX:00 and all the combinations accepted by datetime.

    Args:
        date (str): String representing the date to test

    Returns:
        Boolean True if the date is formatted as ISO 8601
    """
    try:
        datetime.fromisoformat(date)
        return True
    except ValueError:
        return False
