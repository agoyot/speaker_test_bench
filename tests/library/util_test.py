"""
Test util module.
"""
import json
import numpy as np
import pandas as pd
from datetime import datetime

import arrow
import pytest

from speaker_test_bench.library.util import (
    CustomEncoder,
    copy_key_content,
    flatten,
)


def test_unit_custom_encoder_01():
    """
    CustomEncoder convert numpy array into list
    """
    # byte, nan, arrow, datetime, np.datetime64, np.ndarray, np.generic
    in_dict = {
        "byte": bytes(1),
        "byte_list": [bytes(1), 42, bytes(1)],
        "byte_array": np.array([bytes(1), 42, bytes(1)]),
        "nan": float("nan"),
        "nan_list": [float("nan"), 42, float("nan")],
        "nan_array": np.array([float("nan"), 42, float("nan")]),
        "inf": float("inf"),
        "inf_list": [float("inf"), 42, float("inf")],
        "inf_array": np.array([float("inf"), 42, float("inf")]),
        "neg_inf": float("-inf"),
        "neg_inf_list": [float("-inf"), 42, float("-inf")],
        "neg_inf_array": np.array([float("-inf"), 42, float("-inf")]),
        "float64": np.float64(42),
        "float64_list": [np.float64(42), np.float64(42), np.float64(42)],
        "float64_array": np.array([42, 42, 42]).astype(np.float64),
        "tuple": (42, 42, 42),
        "tuple_array": (np.array([42, 42]), np.array([42, 42])),
        "list_array": [np.array([42, 42]), np.array([42, 42])],
        "datetime": datetime(2023, 3, 10, 11, 19, 52),
        "datetime_list": [
            datetime(2023, 3, 10, 11, 19, 52),
            datetime(2023, 3, 10, 11, 19, 52),
            datetime(2023, 3, 10, 11, 19, 52),
        ],
        "datetime_array": np.array(
            [
                datetime(2023, 3, 10, 11, 19, 52),
                datetime(2023, 3, 10, 11, 19, 52),
                datetime(2023, 3, 10, 11, 19, 52),
            ]
        ),
        "datetime64": np.datetime64("2023-03-10T11:19:52.560"),
        "datetime64_list": [
            np.datetime64("2023-03-10T11:19:52.560"),
            np.datetime64("2023-03-10T11:19:52.560"),
            np.datetime64("2023-03-10T11:19:52.560"),
        ],
        "datetime64_array": np.array(
            [
                np.datetime64("2023-03-10T11:19:52.560"),
                np.datetime64("2023-03-10T11:19:52.560"),
                np.datetime64("2023-03-10T11:19:52.560"),
            ]
        ),
        "arrow": arrow.Arrow(2023, 3, 10, 11, 19, 52),
        "arrow_list": [
            arrow.Arrow(2023, 3, 10, 11, 19, 52),
            arrow.Arrow(2023, 3, 10, 11, 19, 52),
            arrow.Arrow(2023, 3, 10, 11, 19, 52),
        ],
        "arrow_array": np.array(
            [
                arrow.Arrow(2023, 3, 10, 11, 19, 52),
                arrow.Arrow(2023, 3, 10, 11, 19, 52),
                arrow.Arrow(2023, 3, 10, 11, 19, 52),
            ]
        ),
        "df": pd.DataFrame(data=[42, 42, 42], columns=["a"]),
        "df_list": [
            pd.DataFrame(data=[42, 42, 42], columns=["a"]),
            pd.DataFrame(data=[42, 42, 42], columns=["a"]),
        ],
        "series": pd.Series(data=[42, 42, 42]),
        "series_list": [
            pd.Series(data=[42, 42, 42]),
            pd.Series(data=[42, 42, 42]),
            pd.Series(data=[42, 42, 42]),
        ],
        "misc": [
            bytes(1),
            float("nan"),
            float("inf"),
            float("-inf"),
            np.array([42, 42]),
            np.float64(42),
            (42, 42),
            datetime(2023, 3, 10, 11, 19, 52),
            np.datetime64("2023-03-10T11:19:52.560"),
            arrow.Arrow(2023, 3, 10, 11, 19, 52),
            pd.DataFrame(data=[42, 42, 42], columns=["a"]),
            pd.Series(data=[42, 42, 42]),
        ],
    }

    out_dict = {
        "byte": "\x00",
        "byte_list": ["\x00", 42, "\x00"],
        "byte_array": ["", "42", ""],
        "nan": None,
        "nan_list": [None, 42, None],
        "nan_array": [None, 42.0, None],
        "inf": None,
        "inf_list": [None, 42, None],
        "inf_array": [None, 42.0, None],
        "neg_inf": None,
        "neg_inf_list": [None, 42, None],
        "neg_inf_array": [None, 42.0, None],
        "float64": 42.0,
        "float64_list": [42.0, 42.0, 42.0],
        "float64_array": [42.0, 42.0, 42.0],
        "tuple": [42, 42, 42],
        "tuple_array": [[42, 42], [42, 42]],
        "list_array": [[42, 42], [42, 42]],
        "datetime": "2023-03-10T11:19:52+00:00",
        "datetime_list": [
            "2023-03-10T11:19:52+00:00",
            "2023-03-10T11:19:52+00:00",
            "2023-03-10T11:19:52+00:00",
        ],
        "datetime_array": [
            "2023-03-10T11:19:52+00:00",
            "2023-03-10T11:19:52+00:00",
            "2023-03-10T11:19:52+00:00",
        ],
        "datetime64": "2023-03-10T11:19:52.560000+00:00",
        "datetime64_list": [
            "2023-03-10T11:19:52.560000+00:00",
            "2023-03-10T11:19:52.560000+00:00",
            "2023-03-10T11:19:52.560000+00:00",
        ],
        "datetime64_array": [
            "2023-03-10T11:19:52.560000+00:00",
            "2023-03-10T11:19:52.560000+00:00",
            "2023-03-10T11:19:52.560000+00:00",
        ],
        "arrow": "2023-03-10T11:19:52+00:00",
        "arrow_list": [
            "2023-03-10T11:19:52+00:00",
            "2023-03-10T11:19:52+00:00",
            "2023-03-10T11:19:52+00:00",
        ],
        "arrow_array": [
            "2023-03-10T11:19:52+00:00",
            "2023-03-10T11:19:52+00:00",
            "2023-03-10T11:19:52+00:00",
        ],
        "df": {"a": {"0": 42, "1": 42, "2": 42}},
        "df_list": [
            {"a": {"0": 42, "1": 42, "2": 42}},
            {"a": {"0": 42, "1": 42, "2": 42}},
        ],
        "series": [42, 42, 42],
        "series_list": [
            [42, 42, 42],
            [42, 42, 42],
            [42, 42, 42],
        ],
        "misc": [
            "\x00",
            None,
            None,
            None,
            [42, 42],
            42.0,
            [42, 42],
            "2023-03-10T11:19:52+00:00",
            "2023-03-10T11:19:52.560000+00:00",
            "2023-03-10T11:19:52+00:00",
            {"a": {"0": 42, "1": 42, "2": 42}},
            [42, 42, 42],
        ],
    }
    assert json.loads(json.dumps(in_dict, cls=CustomEncoder)) == out_dict


flatten_test_data = [
    ([1, 2, [3, 4, [5, 6, 7]]], [1, 2, 3, 4, 5, 6, 7]),
    (["a", ["b"], ["c", "d"], "e"], ["a", "b", "c", "d", "e"]),
    ([{"test_key": 3}, [3, 4], "test"], [{"test_key": 3}, 3, 4, "test"]),
]


@pytest.mark.parametrize("in_list, flat_list", flatten_test_data)
def test_unit_flatten_01(in_list, flat_list):
    assert flatten(in_list) == flat_list


@pytest.mark.parametrize(
    "src_dict, target_dict, key, res",
    [
        (
            {"metadata": {"opmode": 3}},
            {},
            "metadata",
            {"metadata": {"opmode": 3}},
        ),
        (
            {"metadata": {"opmode": 3}},
            {"metadata": {"asset_id": "tagada"}},
            "metadata",
            {"metadata": {"opmode": 3, "asset_id": "tagada"}},
        ),
    ],
)
def test_unit_copy_key_content_01(src_dict, target_dict, key, res):
    """Test regular behavior of the copy_key_content function"""
    copy_key_content(src_dict, target_dict, key, inplace=True)
    assert target_dict == res


def test_unit_copy_key_content_02():
    """Test regular behavior of the copy_key_content function"""
    out_dict = copy_key_content(
        {"metadata": {"opmode": 3}}, {}, "metadata", inplace=False
    )
    assert out_dict == {"metadata": {"opmode": 3}}


def test_robust_key_content_01():
    with pytest.raises(KeyError):
        copy_key_content(
            {"metadata": {"opmode": 3}}, {}, "tagada", inplace=True
        )
