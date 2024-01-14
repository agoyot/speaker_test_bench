"""
speaker_test_bench: TO BE DEFINED (TBD)
==========================================
Documentation is available in the docstrings of each module.

Contents
--------
speaker_test_bench imports all the functions necessary to TBD

Subpackages
-----------
Using any of these subpackages requires an explicit import.

Here is the subpackages list::

 data           --- TBD
 

Utility tools
-------------
::
 __version__    --- speaker_test_bench version string
"""
import importlib as _importlib
import logging

# Uncomment this line when using project
# from speaker_test_bench.version import version as __version__

logger = logging.getLogger(__name__)

submodule_list = ["features", "model", "visualization"]

__all__ = submodule_list + [
    "__version__",
]


def __dir__():
    return __all__


def __getattr__(name):
    if name in submodule_list:
        return _importlib.import_module(f"speaker_test_bench.{name}")
    else:
        try:
            return globals()[name]
        except KeyError as exc:
            raise AttributeError(
                f"Module 'hvac' has no attribute '{name}'"
            ) from exc

