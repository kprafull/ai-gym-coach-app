import importlib


def test_app_imports() -> None:
    importlib.import_module("app")
