import importlib

import jarvis

SUBPACKAGES = ["trigger", "stt", "brain", "tts", "tools", "interfaces"]


def test_version_is_set():
    assert jarvis.__version__


def test_subpackages_import():
    for name in SUBPACKAGES:
        importlib.import_module(f"jarvis.{name}")
