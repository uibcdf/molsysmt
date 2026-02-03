from __future__ import annotations

import inspect
import pkgutil
from importlib import import_module
from types import ModuleType
from typing import Any, Callable, Iterable
from functools import lru_cache

from .argument_registry import ArgumentRegistry


def resolve_standardizer(standardizer: Any) -> Callable[[str, dict[str, Any]], dict[str, Any]] | None:
    if standardizer is None:
        return None
    if callable(standardizer):
        return standardizer
    if isinstance(standardizer, str):
        module_path, _, attr = standardizer.partition(":")
        if not attr:
            module_path, _, attr = standardizer.rpartition(".")
        if not module_path or not attr:
            raise ValueError("standardizer must be a callable or 'module.path:function'")
        module = import_module(module_path)
        fn = getattr(module, attr)
        if not callable(fn):
            raise TypeError("standardizer must resolve to a callable")
        return fn
    raise TypeError("standardizer must be a callable, a string, or None")


def _coerce_sources(source: str | Iterable[str] | None) -> list[str]:
    if source is None:
        return []
    if isinstance(source, str):
        return [source]
    return list(source)


def _merge_digesters(target: dict[str, Callable[..., Any]],
                     incoming: dict[str, Callable[..., Any]]) -> None:
    for name, fn in incoming.items():
        if name not in target:
            target[name] = fn


@lru_cache(maxsize=None)
def _load_from_registry(module_path: str) -> dict[str, Callable[..., Any]]:
    module = import_module(module_path)
    digesters = getattr(module, "ARGUMENT_DIGESTERS", None)
    if digesters is None:
        return {}
    if not isinstance(digesters, dict):
        raise TypeError("ARGUMENT_DIGESTERS must be a dict")
    return dict(digesters)


@lru_cache(maxsize=None)
def _load_from_package(package_path: str) -> dict[str, Callable[..., Any]]:
    package = import_module(package_path)
    if not hasattr(package, "__path__"):
        return {}
    output: dict[str, Callable[..., Any]] = {}
    for module_info in pkgutil.iter_modules(package.__path__):
        module = import_module(f"{package_path}.{module_info.name}")
        _collect_digesters_from_module(module, output)
    return output


def _collect_digesters_from_module(module: ModuleType,
                                   output: dict[str, Callable[..., Any]]) -> None:
    for name, fn in inspect.getmembers(module, inspect.isfunction):
        if not name.startswith("digest_"):
            continue
        arg_name = name[len("digest_"):]
        output[arg_name] = fn


def load_argument_digesters(
    digestion_source: str | Iterable[str] | None,
    digestion_style: str,
) -> dict[str, Callable[..., Any]]:
    sources = _coerce_sources(digestion_source)
    style = digestion_style
    output: dict[str, Callable[..., Any]] = {}

    if style == "decorator":
        _merge_digesters(output, ArgumentRegistry.get_all())
        return output

    if style == "registry":
        for source in sources:
            _merge_digesters(output, _load_from_registry(source))
        return output

    if style == "package":
        for source in sources:
            _merge_digesters(output, _load_from_package(source))
        return output

    if style != "auto":
        raise ValueError("digestion_style must be 'auto', 'registry', 'package', or 'decorator'")

    # auto: registry -> package -> decorator, with source order priority
    for source in sources:
        _merge_digesters(output, _load_from_registry(source))
        _merge_digesters(output, _load_from_package(source))

    _merge_digesters(output, ArgumentRegistry.get_all())
    return output
